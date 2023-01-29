defmodule Derailed.Ready do
  @moduledoc false

  def handle_for(session_pid) do
    Derailed.Session.sync_guilds(session_pid)
    :ok
  end

  # TODO
  def verify_token(token) do
  end
end
