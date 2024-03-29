defmodule Derailed.Guild.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    Dotenv.load!()

    children = [
      {GenRegistry, worker_module: Derailed.Guild}
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Derailed.Guild.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
