use base64::{engine::general_purpose, Engine as _};
use itsdangerous::{default_builder, IntoTimestampSigner, TimestampSigner};

#[rustler::nif]
fn is_valid(user_id: i64, password: String, token: String) -> bool {
    let signer = default_builder(password).build().into_timestamp_signer();
    let user_id = user_id.to_string();

    let unsigned = signer.unsign(&token);

    if let Ok(unsigned) = unsigned {
        let b64_user_id = unsigned.value().to_string();

        match general_purpose::URL_SAFE.decode(b64_user_id) {
            Ok(v) => {
                let value = std::str::from_utf8(v.as_slice()).unwrap();

                value == user_id
            }
            Err(_) => false,
        }
    } else {
        false
    }
}

rustler::init!("Elixir.Derailed.Auth", [is_valid]);
