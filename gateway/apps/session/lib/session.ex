defmodule Derailed.Session do
  @moduledoc """
  Documentation for `Derailed.Session`.
  """

  use GenServer
  require Logger

  @spec start_link(pid(), pid(), integer()) :: {:ok, pid}
  def start_link(session_id, ws_pid, user_id) do
    Logger.debug("Spinning up new Session: #{inspect(session_id)}/#{inspect(ws_pid)}/#{user_id}")
    GenServer.start_link(__MODULE__, {session_id, ws_pid, user_id})
  end

  @spec init({any, atom | pid | {atom, atom}, any}) ::
          {:ok,
           %{
             disconnected: false,
             guild_pids: map(),
             presence_pids: map(),
             id: integer(),
             user_id: any,
             ws_pid: atom | pid | {atom, atom},
             ws_ref: reference(),
             guild_refs: map(),
             presence_refs: map(),
             activities: list(),
             status: integer()
           }}
  def init({session_id, ws_pid, user_id}) do
    ref = ZenMonitor.monitor(ws_pid)

    {:ok,
     %{
       id: session_id,
       guild_pids: Map.new(),
       presence_pids: Map.new(),
       ws_pid: ws_pid,
       user_id: user_id,
       disconnected: false,
       ws_ref: ref,
       guild_refs: Map.new(),
       presence_refs: Map.new(),
       activities: [],
       status: -1
     }}
  end

  def generate_session_id do
    random_data = for _ <- 1..30, do: Enum.random(0..255)

    cap = &:crypto.hash(:md5, &1)

    random_data
    |> cap.()
    |> Base.encode16(case: :lower)
  end

  @spec verify_token!(String.t()) :: map()
  def verify_token!(token) do
    # any errors here the WebSocket interface can handle.
    [encoded_uid, _, _] = String.split(token, ".")
    user_id = encoded_uid |> Base.url_decode64!()
    db_user_id = String.to_integer(user_id)

    stmt = Postgrex.prepare!(:db, "get_user", "SELECT * FROM users WHERE id = $1")
    result = Derailed.Utils.map!(Postgrex.execute!(:db, stmt, [db_user_id]))

    if result == Map.new() do
      raise "User has invalid token information"
    end

    if Derailed.Auth.is_valid(result.id, result.password, token) == false do
      raise "User has invalid token information"
    end

    Map.delete(Map.delete(result, "deletor_job_id"), "password")
  end

  @spec connect_guilds(pid()) :: {:ok, list(), map()}
  def connect_guilds(pid) do
    GenServer.call(pid, :connect_guilds)
  end

  @spec get_presence_pids(pid()) :: list(pid())
  def get_presence_pids(pid) do
    GenServer.call(pid, :get_presence_pids)
  end

  @spec setup_guilds(pid(), list(), list(), list(), map(), integer()) :: :ok
  def setup_guilds(pid, guilds, members, activities, user, status) do
    mems =
      Enum.map(members, fn member ->
        {member.guild_id, member}
      end)

    GenServer.cast(pid, {:setup_guilds, guilds, mems, activities, user, status})
  end

  def handle_call(:connect_guilds, state) do
    stmt =
      Postgrex.prepare!(
        :db,
        "get_guilds_of_user",
        "SELECT * FROM guilds WHERE id IN (SELECT guild_id FROM members WHERE user_id = $1);"
      )

    stmt2 =
      Postgrex.prepare!(:db, "get_user_members", "SELECT * FROM members WHERE user_id = $1;")

    members = Derailed.Utils.map!(Postgrex.execute!(:db, stmt2, [state.user_id]))

    results = Derailed.Utils.maps!(Postgrex.execute!(:db, stmt, [state.user_id]))

    {:reply, {:ok, results, members}, state}
  end

  def handle_call(:get_presence_pids, state) do
    {:reply, state.presence_pids, state}
  end

  def handle_cast({:setup_guilds, guilds, members, activities, user, status}, state) do
    pids =
      Enum.map(guilds, fn guild ->
        {:ok, pid} = GenRegistry.lookup_or_start(Derailed.Guild, guild.id, [guild.id])

        {guild.id, pid}
      end)

    presence_pids =
      Enum.map(guilds, fn guild ->
        {:ok, pid} = GenRegistry.lookup_or_start(Derailed.PresenceTracker, guild.id, [guild.id])

        Derailed.PresenceTracker.subscribe(pid, self(), user.id)

        if status != 2 do
          Derailed.PresenceTracker.publish_presence(pid, user.id, %{
            user: user,
            status: status,
            activities: activities
          })
        end

        {guild.id, pid}
      end)

    refs =
      Enum.map(pids, fn {guild_id, pid} ->
        ref = ZenMonitor.monitor(pid)

        {ref, guild_id}
      end)

    presence_refs =
      Enum.map(presence_pids, fn {guild_id, pid} ->
        ref = ZenMonitor.monitor(pid)

        {ref, guild_id}
      end)

    Enum.each(guilds, fn guild ->
      Manifold.send(
        state.ws_pid,
        {:publish, %{t: "GUILD_CREATE", d: Map.put(guild, "member", Map.get(members, guild.id))}}
      )
    end)

    {:noreply,
     %{
       state
       | guild_pids: pids,
         guild_refs: refs,
         presence_pids: presence_pids,
         presence_refs: presence_refs,
         activities: activities,
         status: status
     }}
  end

  def handle_info({:DOWN, ref, :process, pid, {:zen_monitor, _reason}}, state) do
    if ref == state.ws_ref do
      Logger.debug("WebSocket down, shutting down in 120 seconds unless resumed")

      :erlang.send_after(120_000, self(), :end_session_if_disconnected)

      {:noreply,
       %{
         state
         | ws_pid: nil,
           disconnected: true
       }}
    end

    if Map.get(state.guild_refs, ref) != nil do
      # TODO: handle guild process failure
      Manifold.send(
        state.ws_pid,
        {:publish, %{t: "GUILD_DELETE", d: %{guild_id: Map.get(state.guild_refs, ref)}}}
      )

      {:noreply, state}
    else
      guild_id = Map.get(state.presence_refs, ref)
      presence_pid = GenRegistry.lookup_or_start(Derailed.PresenceTracker, guild_id, [guild_id])
      new_ref = ZenMonitor.monitor(presence_pid)

      presence_pids = Map.delete(state.presence_pids, pid)
      presence_pids = Map.put(presence_pids, guild_id, presence_pid)

      presence_refs = Map.delete(state.presence_refs, ref)
      presence_refs = Map.put(presence_refs, new_ref, guild_id)

      {:noreply,
       %{
         state
         | presence_pids: presence_pids,
           presence_refs: presence_refs
       }}
    end
  end

  def handle_info(:end_session_if_disconnected, state) do
    Logger.debug("Checking if ws_pid is still disconnected")

    if state.disconnected == true do
      Logger.debug("ws_pid is still disconnected, shutting down self")
      {:ok, pid} = GenRegistry.lookup(Derailed.Session.Registry, state.user_id)

      Derailed.Session.Registry.remove_session(pid, state.id)

      GenRegistry.stop(Derailed.Session, state.id)
    end

    {:noreply, state}
  end

  def handle_info({:publish, message}, state) do
    if state.ws_pid != nil do
      Logger.debug("Publishing message #{inspect(message)} to ws_pid")
      Manifold.send(state.ws_pid, {:publish, message})
    end

    t = Map.get(message, "t")

    case t do
      "GUILD_CREATE" ->
        {:ok, pid} = GenRegistry.lookup_or_start(Derailed.Guild, message.d.id, [message.d.id])

        {:ok, presence_pid} =
          GenRegistry.lookup_or_start(Derailed.PresenceTracker, message.d.id, [message.d.id])

        Derailed.Guild.subscribe(pid, self(), state.user_id)
        Derailed.PresenceTracker.subscribe(presence_pid, self(), state.user_id)

        ref = ZenMonitor.monitor(pid)
        pres_ref = ZenMonitor.monitor(presence_pid)

        if state.status != 1 do
          Derailed.PresenceTracker.publish_presence(presence_pid, state.user_id, %{
            user_id: state.user_id,
            activities: state.activities,
            status: state.status
          })
        end

        {:noreply,
         %{
           state
           | guild_pids: Map.put(state.guild_pids, message.d.id, pid),
             presence_pids: Map.put(state.presence_pids, message.d.id, presence_pid),
             guild_refs: Map.put(state.guild_refs, ref, message.d.id),
             presence_refs: Map.put(state.presence_refs, pres_ref, message.d.id)
         }}

      "GUILD_DELETE" ->
        # TODO: make actually work.
        {:ok, pid} = GenRegistry.lookup_or_start(Derailed.Guild, message.d.id, [message.d.id])

        {:ok, presence_pid} =
          GenRegistry.lookup_or_start(Derailed.PresenceTracker, message.d.id, [message.d.id])

        Derailed.Guild.unsubscribe(pid, self())
        Derailed.PresenceTracker.unsubscribe(presence_pid, self())

        ref = ZenMonitor.demonitor(pid, Map.get(state.guild_pids, message.d.guild_id))
        pres_ref = ZenMonitor.demonitor(presence_pid)

        {:noreply,
         %{
           state
           | guild_pids: Map.delete(state.guild_pids, message.d.id),
             presence_pids: Map.delete(state.presence_pids, message.d.id),
             guild_refs: Map.delete(state.guild_refs, ref),
             presence_refs: Map.delete(state.presence_refs, pres_ref)
         }}

      _ ->
        {:noreply, state}
    end
  end

  def handle_info({:setup_guilds, guilds, members, activities, partial_user, status}, state) do
    Derailed.Session.setup_guilds(self(), guilds, members, activities, partial_user, status)

    {:noreply, state}
  end
end
