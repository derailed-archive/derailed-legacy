defmodule Derailed.GRPC.Guild.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      GRPC.Server.Supervisor.child_spec(Derailed.GRPC.Guild.Endpoint, 50051)
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Derailed.GRPC.Guild.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
