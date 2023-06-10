defmodule SessionTest do
  use ExUnit.Case
  doctest Session

  test "greets the world" do
    assert Session.hello() == :world
  end
end
