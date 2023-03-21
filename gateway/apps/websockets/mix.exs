defmodule Derailed.WebSocket.MixProject do
  use Mix.Project

  def project do
    [
      app: :websockets,
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
      mod: {Derailed.WebSocket.Application, []}
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      {:sessions, in_umbrella: true},
      {:ready, in_umbrella: true},
      {:cowboy, "~> 2.9"},
      {:jsonrs, "~> 0.3.0"},
      {:ex_json_schema, "~> 0.9.2"},
      {:guilds, in_umbrella: true},
      {:presences, in_umbrella: true}
    ]
  end
end
