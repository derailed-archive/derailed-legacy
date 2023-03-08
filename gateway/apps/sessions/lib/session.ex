defmodule Derailed.Session do
  use GenServer
  require Logger
  import Ecto.Query

  @spec start_link(pid(), pid(), integer()) :: {:ok, pid}
  def start_link(session_id, ws_pid, user_id) do
    Logger.debug "Spinning up new Session: #{inspect(session_id)}/#{inspect(ws_pid)}/#{user_id}"
    GenServer.start_link(__MODULE__, {session_id, ws_pid, user_id})
  end

  @spec init({any, atom | pid | {atom, atom}, any}) ::
          {:ok,
           %{
             down: false,
             guild_pids: %{},
             id: integer(),
             user_id: any,
             ws_pid: atom | pid | {atom, atom}
           }}
  def init({session_id, ws_pid, user_id}) do
    ZenMonitor.monitor(ws_pid)

    {:ok,
     %{
       id: session_id,
       guild_pids: Map.new(),
       ws_pid: ws_pid,
       user_id: user_id,
       down: false
     }}
  end

  def sync_guilds(pid) do
    GenServer.cast(pid, :sync_guilds)
  end

  def resume(pid, ws_pid) do
    GenServer.cast(pid, {:resume_session, ws_pid})
  end

  # server
  def handle_cast(:sync_guilds, state) do
    Logger.debug "Syncing Guilds"
    joined_guild_member_objects_query =
      from(m in Derailed.Database.Member,
        where: m.user_id == ^state.user_id,
        select: m
      )

    status_setting_query =
      from(us in Derailed.Database.Settings,
        where: us.user_id == ^state.user_id,
        select: us
      )

    activities_query =
      from(
        act in Derailed.Database.Activity,
        where: act.user_id == ^state.user_id,
        select: act
      )

    # this isn't really complex but all it does is:
    # query the db and maps the returned objects to only have the guild ids
    joined_guild_member_objects = Derailed.Database.Repo.all(joined_guild_member_objects_query)
    activity_objects = Derailed.Database.Repo.all(activities_query)

    settings =
      Map.delete(Map.from_struct(Derailed.Database.Repo.one(status_setting_query)), :__meta__)

    guild_ids = Enum.map(joined_guild_member_objects, fn gm -> gm.guild_id end)

    activities =
      Enum.map(activity_objects, fn activity ->
        Map.delete(Map.from_struct(activity), :__meta__)
      end)

    Enum.each(guild_ids, fn guild_id ->
      get_guild_query =
        from(g in Derailed.Database.Guild,
          where: g.id == ^guild_id,
          select: g
        )
      get_channels_query =
        from(c in Derailed.Database.Channel,
          where: c.guild_id == ^guild_id,
          select: c
        )

      chobjs = Derailed.Database.Repo.all(get_channels_query)
      channel_objects = Enum.map(chobjs, fn channel ->
        Map.delete(Map.from_struct(channel), :__meta__)
      end)

      guild_object =
        Map.delete(Map.from_struct(Derailed.Database.Repo.one(get_guild_query)), :__meta__)
      guild_object = Map.put(guild_object, "channels", channel_objects)

      {:ok, guild_pid} = GenRegistry.lookup_or_start(Derailed.Guild, guild_object.id, [guild_object.id])
      Derailed.Guild.subscribe(guild_pid, self(), state.id)

      {:ok, guild_presences_pid} =
        GenRegistry.lookup_or_start(Derailed.Presence.Guild, guild_object.id, [guild_object.id])

      if settings.status != "offline" do
        Derailed.Presence.Guild.publish(
          guild_presences_pid,
          state.user_id,
          settings.status,
          activities
        )
      end

      Manifold.send(state.ws_pid, {:i1_s, %{t: "GUILD_CREATE", d: guild_object}})

      Derailed.Presence.Guild.get_presences(guild_presences_pid, self())
    end)

    {:noreply, state}
  end

  def handle_cast({:resume_session, ws_pid}, state) do
    Logger.debug "Resuming Session, new ws_pid: #{inspect(ws_pid)}"
    {:noreply, %{state | down: false, ws_pid: ws_pid}}
  end

  def handle_info({:DOWN, _ref, :process, _pid, {:zen_monitor, _reason}}, state) do
    Logger.debug "WebSocket down, shutting down in 120 seconds unless resumed"

    :erlang.send_after(120_000, self(), :sip)

    {:noreply,
     %{
       state
       | ws_pid: nil,
         down: true
     }}
  end

  def handle_info(:sip, state) do
    Logger.debug "Checking if ws_pid is still down"
    if state.down == true do
      Logger.debug "ws_pid is still down, shutting down self"
      {:ok, pid} = GenRegistry.lookup(Derailed.Session.Registry, state.user_id)

      Derailed.Session.Registry.remove_session(pid, state.id)

      GenRegistry.stop(Derailed.Session, state.id)
    end

    {:noreply, state}
  end

  def handle_info({:publish, message}, state) do
    # TODO: handle ws_pid being nil
    Logger.debug "Publishing message #{inspect(message)} to ws_pid"
    Manifold.send(state.ws_pid, {:i1_s, message})

    {:noreply, state}
  end
end
