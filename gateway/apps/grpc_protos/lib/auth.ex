defmodule Derailed.GRPC.Auth.Proto.ValidateToken do
  use Protobuf, protoc_gen_elixir_version: "1.14.0", syntax: :proto3

  field(:user_id, 1, type: :string)
  field(:password, 2, type: :string)
  field(:token, 3, type: :string)
end

defmodule Derailed.GRPC.Auth.Proto.Valid do
  use Protobuf, protoc_gen_elixir_version: "1.14.0", syntax: :proto3

  field(:valid, 1, type: :bool)
end

defmodule Derailed.GRPC.Auth.Proto.Service do
  use GRPC.Service, name: "derailed.grpc.auth.Authorization", protoc_gen_elixir_version: "0.14.0"

  rpc(:validate, Derailed.GRPC.Auth.Proto.ValidateToken, Derailed.GRPC.Auth.Proto.Valid)
end

defmodule Derailed.GRPC.Auth.Proto.Stub do
  use GRPC.Stub, service: Derailed.GRPC.Auth.Proto.Service
end
