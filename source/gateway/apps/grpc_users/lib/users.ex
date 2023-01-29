defmodule Derailed.GRPC.User do
  @moduledoc false
  use GRPC.Server, service: Derailed.GRPC.User.Proto.Service

  @doc """
  Publishes a message to all of the Sessions of this specific user.
  """
  @spec publish(Derailed.GRPC.User.Proto.UPubl.t(), GRPC.Server.Stream.t()) ::
          Derailed.GRPC.User.Proto.UPublr.t()
  def publish(publish_info, _stream) do
    user_id = publish_info.user_id

    {:ok, message} = Jsonrs.decode(publish_info.message.data)

    case GenRegistry.lookup(Derailed.Session.Registry, user_id) do
      {:ok, session_reg} ->
        {:ok, sessions} = Derailed.Session.Registry.get_sessions(session_reg)

        Enum.each(sessions, &Manifold.send(&1, %{t: publish_info.event, d: message}))

      {:error, :not_found} ->
        :ok
    end

    Derailed.GRPC.User.Proto.UPublr.new(message: "Success")
  end
end
