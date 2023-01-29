defmodule Derailed.GRPC.Guild.Endpoint do
  use GRPC.Endpoint

  intercept(GRPC.Logger.Server)
  run(Derailed.GRPC.Guild)
end
