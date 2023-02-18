defmodule Derailed.Ready.MixProject do
  use Mix.Project

  def project do
    [
      app: :ready,
      version: "0.1.0",
      build_path: "../../_build",
      config_path: "../../config/config.exs",
      deps_path: "../../deps",
      lockfile: "../../mix.lock",
      elixir: "~> 1.14",
      start_permanent: Mix.env() == :prod,
      deps: deps(),
      xref: [exclude: [Derailed.GRPC.Auth.Proto.Stub]]
    ]
  end

  # Run "mix help compile.app" to learn about applications.
  def application do
    [
      extra_applications: [:logger]
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      {:database, in_umbrella: true},
      {:grpc_protos, in_umbrella: true},
      {:sessions, in_umbrella: true},
      {:auth, in_umbrella: true},
      {:fastglobal, "~> 1.0"},
      {:grpc, "~> 0.5"}
    ]
  end
end
