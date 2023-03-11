defmodule Derailed.Session.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      {GenRegistry, worker_module: Derailed.Session.Registry},
      {GenRegistry, worker_module: Derailed.Session},
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Sessions.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
