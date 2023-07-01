# TODO: handle session process crashing

defmodule Derailed.WebSocket do
  @behaviour :cowboy_websocket
  require Logger

  def init(req, state) do
    {:cowboy_websocket, req, state}
  end

  @spec encode(term()) :: binary
  def encode(term) do
    # TODO: zlib support

    Msgpax.pack!(term, iodata: false)
  end

  @spec get_op(integer()) :: atom()
  def get_op(op) do
    %{
      # 0 => :publish,
      1 => :identify,
      # 2 => :resume,
      # 3 => :ack
      4 => :ping
      # 5 => :hello,
    }[op]
  end

  @spec get_message(map(), non_neg_integer(), term()) :: binary
  def get_message(map, j, state) do
    map = Map.put(map, "s", state.s + 1)
    map = Map.put(map, "j", j)
    encode(map)
  end

  def get_hb_interval do
    Enum.random(42_000..48_000)
  end

  @spec hb_timer(non_neg_integer()) :: reference()
  def hb_timer(time) do
    :erlang.send_after(time + 2000, self(), :hb_check)
  end

  def websocket_init(_req) do
    heartbeat_interval = get_hb_interval()
    hb_timer(heartbeat_interval)
    Logger.debug("Started heartbeat timer for interval #{heartbeat_interval}")

    session_id = Derailed.Session.generate_session_id()

    {:reply,
     {:text,
      get_message(
        %{"heartbeat_interval" => heartbeat_interval},
        5,
        %{
          ready: false,
          session_pid: nil,
          heartbeat_interval: heartbeat_interval,
          sequence: 0,
          pinged: false,
          session_id: session_id,
          user_id: nil
        }
      )},
     %{
       ready: false,
       session_pid: nil,
       session_id: session_id,
       heartbeat_interval: heartbeat_interval,
       sequence: 0,
       pinged: false,
       user_id: nil
     }}
  end

  def websocket_handle({:text, content}, state) do
    Logger.debug("Received content #{inspect(content)}")

    case Hammer.check_rate(state.session_id, 60_000, 60) do
      {:allow, _} ->
        case Msgpax.unpack(content) do
          {:ok, message} ->
            op = Map.get(message, "op")
            Logger.debug("Detected OP #{op}")

            if op == nil do
              {:reply, {:close, 5001, "Job must be present in object."}}
            end

            if not Enum.member?(state.op_codes, op) do
              {:reply, {:close, 5002, "Invalid job code"}}
            end

            job({get_op(op), Map.get(message, "d", Map.new())}, state)

          {:error, _reason} ->
            {:reply, {:close, 5000, "Invalid msgpack given"}}
        end

      _ ->
        {:reply, {:close, 5005, "Rate limit error"}}
    end
  end

  def job({:identify, data}, state) do
    if state.ready == true do
      {:reply, {:close, 5003, "WebSocket already ready"}}
    end

    token = Map.get(data, "token")

    if token == nil do
      {:reply, {:close, 5006, "Invalid Token"}}
    end

    try do
      user = Derailed.Session.verify_token!(token)

      pid =
        GenRegistry.start(Derailed.Session, state.session_id, [state.session_id, self(), user.id])

      registry_pid = GenRegistry.lookup_or_start(Derailed.Session.Registry, user.id, [user.id])
      Derailed.Session.Registry.add_session(registry_pid, pid, state.session_id)
      {:ok, guilds, members} = Derailed.Session.connect_guilds(pid)

      stmt =
        Postgrex.prepare!(:db, "get_read_states", "SELECT * FROM read_states WHERE user_id = $1;")

      read_states = Derailed.Utils.maps!(Postgrex.execute!(:db, stmt, [user.id]))

      stmt2 =
        Postgrex.prepare!(:db, "get_settings", "SELECT * FROM user_settings WHERE user_id = $1;")

      settings = Derailed.Utils.map!(Postgrex.execute!(:db, stmt2, [user.id]))

      partial_user = Map.delete(user, "email")

      stmt3 =
        Postgrex.prepare!(:db, "get_settings", "SELECT * FROM activities WHERE user_id = $1;")

      activities = Derailed.Utils.maps!(Postgrex.execute!(:db, stmt3, [user.id]))

      :erlang.send_after(
        3_000,
        pid,
        {:setup_guilds, guilds, members, activities, partial_user, settings.status}
      )

      {:reply,
       {:text,
        get_message(
          %{
            user: user,
            guilds: guilds,
            members: members,
            v: "1",
            mode: "msgpack",
            read_states: read_states,
            settings: settings,
            activities: activities
          },
          1,
          %{state | ready: true, session_pid: pid, sequence: state.sequence + 1, user_id: user.id}
        )}}
    catch
      "User has invalid token information" -> {:reply, {:close, 5006, "Invalid Token"}}
    end
  end

  def job({:ping, data}, state) do
    if state.pinged == true do
      {:reply, {:close, 5009, "Ping already received"}}
    end

    seq = Map.get(data, "s", 0)

    if state.sequence != seq do
      {:reply, {:close, 5010, "Incorrect sequence"}}
    end

    {:reply,
     {:text,
      get_message(
        %{
          s: 0
        },
        3,
        %{state | sequence: 0}
      )}, %{state | sequence: 0}}
  end

  def websocket_info(:hb_check, state) do
    Logger.debug("Checking heartbeat")

    if state.pinged == true do
      :erlang.send_after(state.heartbeat_interval, self(), :hb_check)
      {:ok, %{state | pinged: false}}
    else
      {:reply, {:close, 5004, "Heartbeat time surpassed"}}
    end
  end

  def terminate(_reason, _req, state) do
    if state.ready == true do
      case GenRegistry.lookup(Derailed.Session.Registry, state.user_id) do
        {:ok, pid} -> Derailed.Session.Registry.remove_session(pid, state.session_pid)
      end

      GenRegistry.stop(Derailed.Session, state.session_id)
    end
  end
end
