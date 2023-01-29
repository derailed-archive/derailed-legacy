defmodule Derailed.MixProject do
  use Mix.Project

  def project do
    [
      apps_path: "apps",
      version: "0.1.0",
      start_permanent: Mix.env() == :prod,
      deps: deps(),
      releases: [
        # different releases for different strategies:
        # stack: the entirety of the Derailed gateway
        # grpc: the entirety of the Derailed gateway's gRPC portion
        # basic: the entirety of the Derailed gateway's Session & Guild portion
        # ws: the entirety of the Derailed gateway's WebSocket portion
        # grpc_users: the gRPC user portion
        # grpc_guilds: the gRPC guild portion
        # guild: the gateway guild portion
        # session: the gateway session portion

        stack: [
          grpc_guilds: :permanent,
          grpc_users: :permanent,
          guilds: :permanent,
          sessions: :permanent,
          database: :permanent
        ],
        grpc: [
          grpc_guilds: :permanent,
          grpc_users: :permanent,
          database: :permanent
        ],
        basic: [
          guilds: :permanent,
          sessions: :permanent,
          database: :permanent
        ],
        # TODO:
        # ws: [],

        grpc_users: [
          grpc_users: :permanent
        ],
        grpc_guilds: [
          grpc_guilds: :permanent
        ],
        guild: [
          guilds: :permanent,
          database: :permanent
        ],
        session: [
          sessions: :permanent,
          database: :permanent
        ]
      ]
    ]
  end

  # Dependencies listed here are available only for this
  # project and cannot be accessed from applications inside
  # the apps folder.
  #
  # Run "mix help deps" for examples and options.
  defp deps do
    [
      {:dotenv, "~> 3.1.0"}
    ]
  end
end
