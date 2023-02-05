import Config

Dotenv.load()

config :database, Derailed.Database.Repo,
  adapter: Ecto.Adapters.Postgres,
  pool_size: 12,
  hostname: System.get_env("PG_HOST", "localhost"),
  port: String.to_integer(System.get_env("PG_PORT", "5432")),
  database: System.get_env("PG_DATABASE", "postgres"),
  username: System.get_env("PG_USERNAME", "postgres"),
  password: System.get_env("PG_PASSWORD", "mysecretpassword"),
  show_sensitive_data_on_connection_error: true
