import Config

Dotenv.load()

config :database, Derailed.Database.Repo,
  adapter: Ecto.Adapters.Postgres,
  url: System.get_env("PG_URI"),
  pool_size: 12,
  database: System.get_env("PG_DATABASE", "postgres"),
  username: System.get_env("PG_USERNAME", "postgres"),
  password: System.get_env("PG_PASSWORD", "mysecretpassword")
