defmodule Derailed.Database.Repo do
  use Ecto.Repo,
    otp_app: :database,
    adapter: Ecto.Adapters.Postgres
end
