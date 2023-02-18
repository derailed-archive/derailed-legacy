defmodule Derailed.Auth do
  use Rustler,
    otp_app: :auth,
    crate: :auth

  @spec is_valid(non_neg_integer(), String.t(), String.t()) :: boolean()
  def is_valid(_user_id, _password, _token), do: :erlang.nif_error(:nif_not_loaded)
end
