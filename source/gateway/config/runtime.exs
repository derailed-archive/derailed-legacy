import Config
import Dotenvy

source!([".env", System.get_env()])

config :database, Derailed.Database.Repo,
  adapter: Ecto.Adapters.Postgres,
  pool_size: 12,
  url: env!("PG_URI", :string!),
  show_sensitive_data_on_connection_error: true
