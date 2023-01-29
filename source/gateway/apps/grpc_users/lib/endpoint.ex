defmodule Derailed.GRPC.User.Endpoint do
  use GRPC.Endpoint

  intercept(GRPC.Logger.Server)
  run(Derailed.GRPC.User)
end
