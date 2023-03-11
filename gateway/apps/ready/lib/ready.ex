defmodule Derailed.Ready do
  @moduledoc false
  import Ecto.Query

  @spec handle_for(pid()) :: :ok
  def handle_for(session_pid) do
    Derailed.Session.sync_guilds(session_pid)
    :ok
  end

  def generate_session_id do
    random_data = for _ <- 1..30, do: Enum.random(0..255)

    cap = &:crypto.hash(:md5, &1)

    random_data
    |> cap.()
    |> Base.encode16(case: :lower)
  end

  def make(user, pid) do
    session_id = generate_session_id()

    {:ok, session_registry_pid} =
      GenRegistry.lookup_or_start(Derailed.Session.Registry, user.id, [user.id])

    {:ok, session_pid} = Derailed.Session.start_link(session_id, pid, user.id)
    Derailed.Session.Registry.add_session(session_registry_pid, session_pid, session_id)
    Derailed.Ready.handle_for(session_pid)

    {:ok, session_pid, session_id, session_registry_pid}
  end

  @spec verify_token(String.t()) :: {:ok, map()} | {:error, :invalid_authorization}
  def verify_token(token) do
    # TODO: handle errors here
    [encoded_uid, _, _] = String.split(token, ".")
    {:ok, user_id} = encoded_uid |> Base.url_decode64()
    db_user_id = String.to_integer(user_id)

    query =
      from(
        u in Derailed.Database.User,
        where: u.id == ^db_user_id,
        select: u
      )

    user = Derailed.Database.Repo.one(query)

    case user do
      nil ->
        {:error, :invalid_authorization}

      ruser ->
        valid = Derailed.Auth.is_valid(user.id, user.password, token)

        case valid do
          true ->
            {:ok, Map.delete(Map.delete(Map.from_struct(ruser), :__meta__), :password)}

          false ->
            {:error, :invalid_authorization}
        end
    end
  end
end
