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
             guild_pids: %{},
             id: integer(),
             user_id: any,
             ws_pid: atom | pid | {atom, atom},
             ws_ref: reference()
           }}
  def init({session_id, ws_pid, user_id}) do
    ref = ZenMonitor.monitor(ws_pid)

    {:ok,
     %{
       id: session_id,
       guild_pids: Map.new(),
       ws_pid: ws_pid,
       user_id: user_id,
       disconnected: false,
       ws_ref: ref
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

    result
  end

  @spec connect_guilds(pid()) :: :ok
  def connect_guilds(pid) do
    GenServer.call(pid, :connect_guilds)
  end

  @spec setup_guilds(pid(), list(), list()) :: :ok
  def setup_guilds(pid, guilds, members) do
    mems =
      Enum.map(members, fn member ->
        {member.guild_id, member}
      end)

    GenServer.cast(pid, {:setup_guilds, guilds, mems})
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

    members = Derailed.Utils.map!(Postgrex.execute!(:db, stmt2, [state.id]))

    results = Derailed.Utils.maps!(Postgrex.execute!(:db, stmt, [state.id]))

    {:reply, {results, members}, state}
  end

  def handle_cast({:setup_guilds, guilds, members}, state) do
    pids =
      Enum.map(guilds, fn guild ->
        {:ok, pid} = GenRegistry.lookup_or_start(Derailed.Guild, guild.id, [guild.id])

        {guild.id, pid}
      end)

    Enum.each(guilds, fn guild ->
      Manifold.send(
        state.ws_pid,
        {:publish, %{t: "GUILD_CREATE", d: Map.put(guild, "member", Map.get(members, guild.id))}}
      )
    end)

    {:noreply, %{state | guild_pids: pids}}
  end

  def handle_info({:publish, message}, state) do
    if state.ws_pid != nil do
      Logger.debug("Publishing message #{inspect(message)} to ws_pid")
      Manifold.send(state.ws_pid, {:publish, message})
    end

    {:noreply, state}
  end
end
