defmodule Derailed.Session.Registry do
  @moduledoc """
  Registry for Derailed Sessions. Used to interconnect a users' sessions.
  """
  use GenServer
  require Logger

  @spec start_link(pid()) :: {:ok, pid}
  def start_link(user_id) do
    Logger.debug("Spinning up new Session Registry: #{inspect(user_id)}")
    GenServer.start_link(__MODULE__, user_id)
  end

  def init(user_id) do
    {:ok,
     %{
       id: user_id,
       session_pids: MapSet.new()
     }}
  end

  @doc """
  Adds a session to this Registry
  """
  @spec add_session(pid(), pid()) :: :ok
  def add_session(pid, session_pid) do
    GenServer.cast(pid, {:add, session_pid})
  end

  @doc """
  Removes a session from this Registry
  """
  @spec remove_session(pid(), pid()) :: :ok
  def remove_session(pid, session_pid) do
    GenServer.cast(pid, {:remove, session_pid})
  end

  @doc """
  Returns every session in this Registry
  """
  @spec get_sessions(pid()) :: {:ok, Enum.t()}
  def get_sessions(pid) do
    GenServer.call(pid, :get_all)
  end

  def handle_cast({:add, session_pid}, state) do
    {:noreply, %{state | session_pids: MapSet.put(state.session_pids, session_pid)}}
  end

  def handle_cast({:remove, session_pid}, state) do
    mps = MapSet.delete(state.session_pids, session_pid)

    if mps == MapSet.new() do
      GenRegistry.stop(Derailed.Session.Registry, state.id)
    end

    {:noreply, %{state | session_pids: mps}}
  end

  def handle_call(:get_all, _from, state) do
    {:reply, {:ok, state.session_pids}, state}
  end
end
