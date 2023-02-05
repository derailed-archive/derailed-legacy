defmodule Derailed.WebSocket.Connection do
  @moduledoc """
  Process to handle a single Derailed websocket connection
  """

  @behaviour :cowboy_websocket
  require Logger

  def init(req, state) do
    {:cowboy_websocket, req, state}
  end

  def map_op(op) do
    %{
      1 => :ready,
      # 2 => :resume,
      3 => :ack
    }[op]
  end

  @spec encode(non_neg_integer() | nil, non_neg_integer() | nil, term() | map()) :: String.t()
  def encode(op, new_sequence, data) do
    {:ok, encoded} = Jsonrs.encode(%{"op" => op, "s" => new_sequence, "d" => data})
    encoded
  end

  def get_hb_interval do
    Enum.random(42_000..48_000)
  end

  @spec hb_timer(non_neg_integer()) :: reference()
  def hb_timer(time) do
    :erlang.send_after(time + 1000, self(), :check_heartbeat)
  end

  def websocket_init(_req) do
    heartbeat_interval = get_hb_interval()
    hb_timer(heartbeat_interval)

    {:reply, {:text, encode(nil, nil, %{"heartbeat_interval" => heartbeat_interval})},
     %{
       ready: false,
       session_pid: nil,
       heartbeat_interval: heartbeat_interval,
       sequence: nil,
       # TODO: add resume
       op_codes: [1, 3],
       ackd: false
     }}
  end

  def websocket_handle({:text, content}, state) do
    case Jsonrs.decode(content) do
      {:ok, message} ->
        op = Map.get(message, "op")

        if op == nil do
          {:close, 5001, "Op code must not be nulled or undefined"}
        end

        if not Enum.member?(state.op_codes, op) do
          {:close, 5002, "Invalid Op code"}
        end

        handle_op({map_op(op), Map.get(message, "d", Map.new())}, state)

      {:error, _reason} ->
        {:close, 5000, "Invalid JSON given"}
    end
  end

  def websocket_handle(_any_frame, state) do
    {:ok, state}
  end

  def websocket_info({:i1_s, message}, state) do
    if state.sequence != nil do
      {:reply, {:text, encode(0, state.sequence + 1, message)},
       %{state | sequence: state.sequence + 1}}
    else
      {:reply, {:text, encode(0, 1, message)}, %{state | sequence: 0}}
    end
  end

  def websocket_info(:check_heartbeat, state) do
    if state.ackd == true do
      :erlang.send_after(state.heartbeat_interval, self(), :check_heartbeat)
      {:ok, %{state | ackd: false}}
    else
      IO.puts(inspect(state))
      {:close, 5006, "Heartbeat time surpassed"}
    end
  end

  def handle_op({:ready, message}, state) do
    if state.ready == false do
      {:close, 5005, "Already ready"}
    end

    if not Map.has_key?(message, "token") do
      {:close, 5003, "No token provided"}
    end

    token = Map.get(message, "token")

    case Derailed.Ready.verify_token(token) do
      {:ok, user} ->
        {:ok, session_pid, session_id} = Derailed.Ready.make(user, self())

        {:reply, {:text, encode(1, nil, %{"user" => user, "session_id" => session_id})},
         %{state | session_pid: session_pid}}

      {:error, :invalid_authorization} ->
        {:close, 5004, "Invalid authorization"}
    end
  end

  def handle_op({:ack, message}, state) do
    if state.ackd == true do
      {:close, 5008, "Already acknowledged this interval"}
    end

    sequence = Map.get(message, "s")

    if state.sequence != sequence do
      {:close, 5007, "Incorrect sequence"}
    else
      {:reply, {:text, encode(3, nil, nil)}, %{state | ackd: true, sequence: nil}}
    end
  end

  def terminate(_reason, _req, state) do
    if state.ready == false do
      :ok
    end
  end
end
