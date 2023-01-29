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

        # grouped
        stack: [
          applications: [
            grpc_guilds: :permanent,
            grpc_users: :permanent,
            guilds: :permanent,
            sessions: :permanent,
            database: :permanent,
            websockets: :permanent
          ]
        ],
        grpc: [
          applications: [
            grpc_guilds: :permanent,
            grpc_users: :permanent,
            database: :permanent
          ]
        ],
        basic: [
          applications: [
            guilds: :permanent,
            sessions: :permanent,
            database: :permanent
          ]
        ],
        ws: [
          applications: [
            websockets: :permanent
          ]
        ],

        # singleton
        grpc_users: [
          applications: [
            grpc_users: :permanent
          ]
        ],
        grpc_guilds: [
          applications: [
            grpc_guilds: :permanent
          ]
        ],
        guild: [
          applications: [
            guilds: :permanent,
            database: :permanent
          ]
        ],
        session: [
          applications: [
            sessions: :permanent,
            database: :permanent
          ]
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
