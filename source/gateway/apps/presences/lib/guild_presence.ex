defmodule Derailed.Presence.Guild do
  use GenServer
  require Logger

  def start_link(guild_id) do
    Logger.debug("Spinning up new Guild Presence: #{inspect(guild_id)}")
    GenServer.start_link(__MODULE__, guild_id)
  end

  def init(guild_id) do
    {:ok,
     %{
       id: guild_id,
       sessions: MapSet.new(),
       presences: Map.new()
     }}
  end

  @spec send(pid(), any()) :: term()
  def send(pid, message) do
    GenServer.call(pid, {:send, message})
  end

  @spec publish(pid(), String.t(), String.t(), list(map())) :: term()
  def publish(
        pid,
        user_id,
        status,
        activities
      ) do
    GenServer.call(pid, {:publish, user_id, status, activities})
  end

  @spec get_presences(pid(), pid()) :: :ok
  def get_presences(pid, session_pid) do
    GenServer.cast(pid, {:get_presences, session_pid})
  end

  # server
  def handle_call({:send, message}, _from, %{sessions: sessions} = state) do
    message = Map.put(message, "guild_id", state.id)

    Enum.each(
      sessions,
      &Manifold.send(&1, {:publish, %{"t" => "PRESENCE_UPDATE", "d" => message}})
    )

    {:reply, :ok, state}
  end

  def handle_call({:publish, user_id, status, activities}, _from, state) do
    data = %{
      "guild_id" => state.id,
      "user_id" => user_id,
      "status" => status,
      "activities" => activities
    }

    Derailed.Presence.Guild.send(self(), data)
    {:reply, :ok, %{state | presences: Map.put(state.presences, user_id, data)}}
  end

  # casted to
  def handle_cast({:get_presences, session_pid}, %{presences: presences} = state) do
    mapped_values = Enum.map(presences, fn {_k, v} -> v end)

    Manifold.send(session_pid, {:publish, %{t: "PRESENCE_BULK_UPDATE", d: mapped_values}})
    {:noreply, state}
  end
end
