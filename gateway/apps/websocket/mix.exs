defmodule Derailed.WebSocket.MixProject do
  use Mix.Project

  def project do
    [
      app: :websocket,
      version: "0.0.0",
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
      mod: {Derailed.WebSocket.Application, []}
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      {:ex_json_schema, "~> 0.9.3"},
      {:cowboy, "~> 2.9"},
      {:msgpax, "~> 2.4.0"},
      {:jsonrs, "~> 0.3.0"},
      {:hammer, "~> 6.1"},
      {:snowflake, "~> 1.0.0"},
      {:guilds, in_umbrella: true},
      {:session, in_umbrella: true},
      {:utils, in_umbrella: true}
    ]
  end
end
