defmodule Derailed.Session.MixProject do
  use Mix.Project

  def project do
    [
      app: :session,
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
      mod: {Derailed.Session.Application, []}
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      {:manifold, "~> 1.6"},
      {:zen_monitor, "~> 2.0"},
      {:gen_registry, "~> 1.3.0"},
      {:postgrex, "~> 0.17.1"},
      {:utils, in_umbrella: true},
      {:auth, in_umbrella: true},
      {:guilds, in_umbrella: true}
    ]
  end
end
