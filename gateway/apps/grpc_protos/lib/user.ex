defmodule Derailed.GRPC.User.Proto.UPubl do
  use Protobuf, protoc_gen_elixir_version: "1.14.0", syntax: :proto3

  field(:user_id, 1, type: :string)
  field(:message, 2, type: Derailed.GRPC.Proto.Message)
end

defmodule Derailed.GRPC.User.Proto.UPublr do
  use Protobuf, protoc_gen_elixir_version: "1.14.0", syntax: :proto3

  field(:message, 1, type: :string)
end

defmodule Derailed.GRPC.User.Proto.Service do
  use GRPC.Service, name: "derailed.grpc.User", protoc_gen_elixir_version: "0.14.0"

  rpc(:publish, Derailed.GRPC.User.Proto.UPubl, Derailed.GRPC.User.Proto.UPublr)
end

defmodule Derailed.GRPC.User.Proto.Stub do
  use GRPC.Stub, service: Derailed.GRPC.User.Proto.Service
end
