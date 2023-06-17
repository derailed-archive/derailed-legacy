defmodule GrpcUsersTest do
  use ExUnit.Case
  doctest GrpcUsers

  test "greets the world" do
    assert GrpcUsers.hello() == :world
  end
end
