defmodule Derailed.GRPC.Guild.MixProject do
  use Mix.Project

  def project do
    [
      app: :grpc_guilds,
      version: "0.1.0",
      build_path: "../../_build",
      config_path: "../../config/config.exs",
      deps_path: "../../deps",
      lockfile: "../../mix.lock",
      elixir: "~> 1.14",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  # Run "mix help compile.app" to learn about applications.
  def application do
    [
      extra_applications: [:logger],
      mod: {Derailed.GRPC.Guild.Application, []}
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      {:gen_registry, "~> 1.3"},
      {:jsonrs, "~> 0.3.0"},
      {:grpc_protos, in_umbrella: true},
      {:guilds, in_umbrella: true},
      {:presences, in_umbrella: true},
      {:dotenv, "~> 3.1.0"},
      {:ex_hash_ring, "~> 6.0"},
      {:fastglobal, "~> 1.0"},
      {:grpc, "~> 0.5"},
      {:zen_monitor, "~> 2.0.2"}
    ]
  end
end
