defmodule Derailed.GRPC.Guild do
  use GRPC.Server, service: Derailed.GRPC.Guild.Proto.Service

  @doc """
  Process responsible for publishing messages to Guilds
  """
  @spec publish(Derailed.GRPC.Guild.Proto.Publ.t(), GRPC.Server.Stream.t()) ::
          Derailed.GRPC.Guild.Proto.Publr.t()
  def publish(publish_info, _stream) do
    guild_id = publish_info.guild_id

    {:ok, message} = Jsonrs.decode(publish_info.message.data)

    case GenRegistry.lookup(Derailed.Guild, guild_id) do
      {:ok, guild_pid} ->
        Derailed.Guild.publish(guild_pid, %{t: publish_info.event, d: message})

      {:error, :not_found} ->
        :ok
    end

    Derailed.GRPC.Guild.Proto.Publr.new(message: "Success")
  end

  @doc """
  Responsible process for `GET /guilds/.../preview` and Invite Previews.
  Returns the amount of presences and if the Guild is available
  """
  @spec get_guild_info(Derailed.GRPC.Guild.Proto.GetGuildInfo, GRPC.Server.Stream.t()) ::
          Derailed.GRPC.Guild.Proto.RepliedGuildInfo.t()
  def get_guild_info(guild, _stream) do
    guild_id = guild.guild_id

    case GenRegistry.lookup(Derailed.Guild, guild_id) do
      {:ok, guild_pid} ->
        {:ok, presences} = Derailed.Guild.get_guild_info(guild_pid)

        Derailed.GRPC.Guild.Proto.RepliedGuildInfo.new(
          presences: presences,
          available: true
        )

      {:error, :not_found} ->
        Derailed.GRPC.Guild.Proto.RepliedGuildInfo.new(
          presences: 0,
          available: false
        )
    end
  end
end
