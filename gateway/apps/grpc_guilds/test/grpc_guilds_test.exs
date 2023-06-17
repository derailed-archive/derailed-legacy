defmodule GrpcGuildsTest do
  use ExUnit.Case
  doctest GrpcGuilds

  test "greets the world" do
    assert GrpcGuilds.hello() == :world
  end
end
