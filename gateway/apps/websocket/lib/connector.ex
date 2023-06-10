defmodule Derailed.WebSocket.Connector do
  def get_dispatch do
    :cowboy_router.compile([
      {:_,
       [
         {"/", Derailed.WebSocket, %{}}
       ]}
    ])
  end

  def start_link do
    {:ok, _} =
      :cowboy.start_clear(
        :derailed_gateway,
        [{:port, 4731}],
        %{
          env: %{
            dispatch: get_dispatch()
          }
        }
      )
  end
end
