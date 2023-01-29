import Config

Dotenv.load()

config :database, Derailed.Database.Repo,
  adapter: Ecto.Adapters.Postgres,
  url: System.get_env("PG_URI"),
  pool_size: 12,
  database: "postgres",
  username: "postgres",
  password: "mysecretpassword"
