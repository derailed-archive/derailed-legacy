defmodule Derailed.Session.Registry do
  @moduledoc """
  Documentation for `Derailed.Session.Registery`.
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
       sessions: Map.new()
     }}
  end

  @doc """
  Adds a session to this Registry
  """
  @spec add_session(pid(), pid(), String.t()) :: :ok
  def add_session(pid, session_pid, session_id) do
    GenServer.cast(pid, {:add, session_pid, session_id})
  end

  @doc """
  Removes a session from this Registry
  """
  @spec remove_session(pid(), String.t()) :: :ok
  def remove_session(pid, session_id) do
    GenServer.cast(pid, {:remove, session_id})
  end

  @doc """
  Returns every session in this Registry
  """
  @spec get_sessions(pid()) :: {:ok, Enum.t()}
  def get_sessions(pid) do
    GenServer.call(pid, :get_all)
  end

  @doc """
  Gets a session from its id
  """
  @spec get_session(pid(), String.t()) :: {:ok, pid() | nil}
  def get_session(pid, session_id) do
    GenServer.call(pid, {:get_one, session_id})
  end

  def handle_cast({:add, session_pid, session_id}, %{sessions: sessions} = state) do
    {:noreply, %{state | sessions: Map.put(sessions, session_id, session_pid)}}
  end

  def handle_cast({:remove, session_id}, %{sessions: sessions} = state) do
    mps = Map.delete(sessions, session_id)

    if mps == Map.new() do
      GenRegistry.stop(Derailed.Session.Registry, state.id)
    end

    {:noreply, %{state | sessions: mps}}
  end

  def handle_call(:get_all, _from, state) do
    {:reply, {:ok, state.session_pids}, state}
  end

  def handle_call({:get_one, session_id}, _from, %{sessions: sessions} = state) do
    {:reply, Map.get(sessions, session_id), state}
  end
end
