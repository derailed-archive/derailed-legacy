defmodule Derailed.Session.MixProject do
  use Mix.Project

  def project do
    [
      app: :sessions,
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
      mod: {Derailed.Session.Application, []}
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      {:manifold, "~> 1.5"},
      {:guilds, in_umbrella: true},
      {:dotenv, "~> 3.1.0"},
      {:ex_hash_ring, "~> 6.0"},
      {:zen_monitor, "~> 2.0.2"},
      {:database, in_umbrella: true}
    ]
  end
end
