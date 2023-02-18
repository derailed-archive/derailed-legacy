defmodule Derailed.GRPC.Proto.Message do
  use Protobuf, protoc_gen_elixir_version: "1.14.0", syntax: :proto3

  field(:event, 1, type: :string)
  field(:data, 2, type: :string)
end

defmodule Derailed.GRPC.Guild.Proto.Publ do
  use Protobuf, protoc_gen_elixir_version: "1.14.0", syntax: :proto3

  field(:guild_id, 1, type: :string)
  field(:message, 2, type: Derailed.GRPC.Proto.Message)
end

defmodule Derailed.GRPC.Guild.Proto.Publr do
  use Protobuf, protoc_gen_elixir_version: "1.14.0", syntax: :proto3

  field(:message, 1, type: :string)
end

defmodule Derailed.GRPC.Guild.Proto.GetGuildInfo do
  use Protobuf, protoc_gen_elixir_version: "1.14.0", syntax: :proto3

  field(:guild_id, 1, type: :string)
end

defmodule Derailed.GRPC.Guild.Proto.RepliedGuildInfo do
  use Protobuf, protoc_gen_elixir_version: "1.14.0", syntax: :proto3

  field(:presences, 1, type: :int32)
  field(:available, 2, type: :bool)
end

defmodule Derailed.GRPC.Guild.Proto.Service do
  use GRPC.Service, name: "derailed.grpc.Guild", protoc_gen_elixir_version: "0.14.0"

  rpc(:publish, Derailed.GRPC.Guild.Proto.Publ, Derailed.GRPC.Guild.Proto.Publr)

  rpc(
    :get_guild_info,
    Derailed.GRPC.Guild.Proto.GetGuildInfo,
    Derailed.GRPC.Guild.Proto.RepliedGuildInfo
  )
end

defmodule Derailed.GRPC.Guild.Proto.Stub do
  use GRPC.Stub, service: Derailed.GRPC.Guild.Proto.Service
end
