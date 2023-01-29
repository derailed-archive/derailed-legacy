defmodule Derailed.DatabaseTest do
  use ExUnit.Case
  doctest Derailed.Database

  test "greets the world" do
    assert Derailed.Database.hello() == :world
  end
end
