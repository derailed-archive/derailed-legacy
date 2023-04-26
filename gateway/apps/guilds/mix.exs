defmodule Derailed.Guild.MixProject do
  use Mix.Project

  def project do
    [
      app: :guilds,
      version: "0.1.0",
      build_path: "../../_build",
      config_path: "../../config/config.exs",
      deps_path: "../../deps",
      lockfile: "../../mix.lock",
      elixir: "~> 1.14",
      start_permanent: Mix.env() == :prod,
      deps: deps(),
      xref: [
        exclude: [
          Derailed.Database.Repo,
          Ecto.Query.Builder,
          Ecto.Query,
          Derailed.Database.Member,
          Derailed.Database.MemberRole
        ]
      ]
    ]
  end

  # Run "mix help compile.app" to learn about applications.
  def application do
    [
      extra_applications: [:logger],
      mod: {Derailed.Guild.Application, []}
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      {:gen_registry, "~> 1.3.0"},
      {:postgrex, "~> 0.17.0"},
      {:dotenv, "~> 3.1.0"},
      {:manifold, "~> 1.6"},
      {:zen_monitor, "~> 2.0.2"},
      {:database, in_umbrella: true},
      {:presences, in_umbrella: true}
    ]
  end
end
