defmodule Derailed.GRPC.Guild do
  use GRPC.Server, service: Derailed.GRPC.Guild.Proto.Service
  require Logger

  @doc """
  Process responsible for publishing messages to Guilds
  """
  @spec publish(Derailed.GRPC.Guild.Proto.Publ.t(), GRPC.Server.Stream.t()) ::
          Derailed.GRPC.Guild.Proto.Publr.t()
  def publish(publish_info, _stream) do
    Logger.debug publish_info
    guild_id = publish_info.guild_id

    {:ok, message} = Jsonrs.decode(publish_info.message.data)

    case GenRegistry.lookup(Derailed.Guild, guild_id) do
      {:ok, guild_pid} ->
        Logger.debug "Guild found"
        Derailed.Guild.publish(guild_pid, %{t: publish_info.event, d: message})

      {:error, :not_found} ->
        Logger.debug "Guild not found"
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
      {:ok, _guild_pid} ->
        {:ok, presence_pid} = GenRegistry.lookup(Derailed.Presence.Guild, guild_id)
        presence_count = Derailed.Presence.Guild.count_presences(presence_pid)

        Derailed.GRPC.Guild.Proto.RepliedGuildInfo.new(
          presences: presence_count,
          available: true
        )

      {:error, :not_found} ->
        case GenRegistry.lookup(Derailed.Presence.Guild, guild_id) do
          {:ok, presence_pid} ->
            Derailed.GRPC.Guild.Proto.RepliedGuildInfo.new(
              presences: Derailed.Presence.Guild.count_presences(presence_pid),
              available: false
            )

          {:error, :not_found} ->
            Derailed.GRPC.Guild.Proto.RepliedGuildInfo.new(
              presences: 0,
              available: false
            )
        end
    end
  end
end
