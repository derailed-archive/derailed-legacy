# these serve as the most minimal db models needed:
# users are served during the READY event, along with settings
# guilds are stored within a guild itself to send to any widbee clients
# members are stored in guilds for fast access of online members
# activities are used for stateful presence updating

defmodule Derailed.Database.User do
  use Ecto.Schema

  @primary_key {:id, :integer, []}

  schema "users" do
    field(:username, :string)
    field(:discriminator, :string)
    field(:email, :string)
    field(:password, :string)
    field(:flags, :integer)
    field(:system, :boolean)
    field(:deletor_job_id, :string)
    field(:suspended, :boolean)
  end
end

defmodule Derailed.Database.Settings do
  use Ecto.Schema

  @primary_key {:user_id, :integer, []}

  schema "settings" do
    field(:status, :string)
  end
end

defmodule Derailed.Database.GuildPosition do
  use Ecto.Schema

  @primary_key false

  schema "guild_positions" do
    field(:user_id, :integer, primary_key: true)
    field(:guild_id, :integer, primary_key: true)
    field(:position, :integer)
  end
end

defmodule Derailed.Database.Guild do
  use Ecto.Schema

  @primary_key {:id, :integer, []}

  schema "guilds" do
    field(:name, :string)
    field(:flags, :integer)
    field(:owner_id, :integer)
    field(:permissions, :integer)
  end
end

defmodule Derailed.Database.Member do
  use Ecto.Schema

  @primary_key false

  schema "members" do
    field(:user_id, :integer)
    field(:guild_id, :integer)
    field(:nick, :string)
  end
end

defmodule Derailed.Database.Activity do
  use Ecto.Schema

  @primary_key {:user_id, :integer, []}

  schema "activities" do
    field(:type, :integer)
    field(:created_at, :utc_datetime)
    field(:content, :string)
  end
end

defmodule Derailed.Database.MemberRole do
  use Ecto.Schema

  @primary_key false

  schema "member_roles" do
    field(:user_id, :integer, primary_key: true)
    field(:role_id, :integer, primary_key: true)
    field(:guild_id, :integer, primary_key: true)
  end
end

defmodule Derailed.Database.Channel do
  use Ecto.Schema

  @primary_key false

  schema "channels" do
    field(:id, :integer, primary_key: true)
    field(:type, :string)
    field(:name, :string)
    field(:last_message_id, :integer)
    field(:parent_id, :integer)
    field(:guild_id, :integer)
    field(:position, :integer)
  end
end
