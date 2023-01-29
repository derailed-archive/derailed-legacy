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
       sessions: MapSet.new()
     }}
  end

  @spec send(pid(), any()) :: :ok
  def send(pid, message) do
    GenServer.call(pid, {:send, message})
  end

  @spec publish(pid(), map(), String.t(), list(map())) :: :ok
  def publish(
        pid,
        user,
        status,
        activities
      ) do
    GenServer.call(pid, {:publish, user, status, activities})
  end

  # server
  def handle_call({:send, message}, _from, %{sessions: sessions} = state) do
    message = Map.put(message, "guild_id", state.id)
    Enum.each(sessions, &Manifold.send(&1, %{"t" => "PRESENCE_UPDATE", "d" => message}))
    {:reply, :ok, state}
  end

  def handle_call({:publish, user, status, activities}, _from, state) do
    data = %{
      "guild_id" => state.id,
      "user" => user,
      "status" => status,
      "activities" => activities
    }

    Derailed.Presence.Guild.send(self(), data)
    {:reply, :ok, state}
  end
end
