defmodule Derailed.Guild do
  @moduledoc """
  Process holding data for an online Guild
  """
  require Logger
  use GenServer
  import Ecto.Query

  # GenServer API

  def start_link(guild_id) do
    Logger.debug("Spinning up new Guild: #{inspect(guild_id)}")
    GenServer.start_link(__MODULE__, guild_id)
  end

  def init(guild_id) do
    {:ok,
     %{
       id: guild_id,
       sessions: Map.new()
     }}
  end

  # Session API
  @spec subscribe(pid(), pid(), integer()) :: :ok
  def subscribe(pid, session_pid, user_id) do
    Logger.debug("Subscribing #{inspect(session_pid)} to #{inspect(pid)}")
    GenServer.cast(pid, {:subscribe, session_pid, user_id})
  end

  @spec unsubscribe(pid(), pid()) :: :ok
  def unsubscribe(pid, session_pid) do
    Logger.debug("Unsubscribing #{inspect(session_pid)} to #{inspect(pid)}")
    GenServer.cast(pid, {:unsubscribe, session_pid})
  end

  # shared API between gRPC and Sessions
  @spec publish(pid(), any()) :: :ok
  def publish(pid, message) do
    Logger.debug("Publishing #{inspect(message)} to #{inspect(pid)}")
    GenServer.call(pid, {:publish, message})
  end

  # backend server api
  def handle_cast({:subscribe, pid, user_id}, state) do
    ZenMonitor.monitor(pid)
    {:noreply, %{state | sessions: Map.put(state.sessions, pid, %{pid: pid, user_id: user_id})}}
  end

  def handle_cast({:unsubscribe, pid}, state) do
    nmp = Map.delete(state.sessions, pid)
    ZenMonitor.demonitor(pid)

    if nmp == Map.new() do
      GenRegistry.stop(Derailed.Guild, state.id)
    end

    {:noreply, %{state | sessions: nmp}}
  end

  def handle_call({:get_guild_members, session_pid}, state) do
    member_query =
      from(m in Derailed.Database.Member,
        where: m.guild_id == ^state.id,
        select: m
      )

    members = Derailed.Database.Repo.all(member_query)

    members =
      Enum.map(members, fn m ->
        member = Map.new(m)

        roles_query =
          from(mr in Derailed.Database.MemberRole,
            where: mr.user_id == ^member.id,
            where: mr.guild_id == ^state.id,
            select: mr.role_id
          )

        roles_lick = Derailed.Database.Repo.all(roles_query)

        roles =
          Enum.map(roles_lick, fn rl ->
            rl.role_id
          end)

        user_query =
          from(u in Derailed.Database.User,
            where: u.id == ^member.id,
            select: u
          )

        user =
          Map.delete(
            Map.delete(Map.from_struct(Derailed.Database.Repo.one(user_query)), :password),
            :__meta__
          )

        member = Map.put(member, "roles", roles)
        member = Map.delete(member, "user_id")
        Map.put(member, "user", user)
      end)

    Manifold.send(
      session_pid,
      {:publish,
       %{
         "t" => "MEMBER_CACHE_UPDATE",
         "d" => %{"guild_id" => state.guild_id, "members" => members}
       }}
    )
  end

  def handle_call({:publish, message}, _from, %{sessions: sessions} = state) do
    Enum.each(Map.values(sessions), &Manifold.send(&1.pid, {:publish, message}))
    {:reply, :ok, state}
  end

  def handle_info({:DOWN, _ref, :process, pid, {:zen_monitor, _reason}}, state) do
    {:noreply,
     %{
       state
       | sessions: Map.delete(state.sessions, pid)
     }}
  end
end
