defmodule Derailed.Gateway.Connector do
  def get_dispatch do
    :cowboy_router.compile([
      {:_,
       [
         {"/", Derailed.WebSocket.Connection, %{}}
       ]}
    ])
  end

  def start_link do
    {:ok, _} =
      :cowboy.start_clear(
        :derailed_gateway,
        [{:port, 10000}],
        %{
          env: %{
            dispatch: get_dispatch()
          }
        }
      )
  end
end
