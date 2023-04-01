/*
    SPDX-License-Identifier: AGPL-3.0
    Copyright 2021-2023 Derailed
*/

use base64::{engine::general_purpose, Engine as _};
use itsdangerous::{default_builder, IntoTimestampSigner, TimestampSigner};

use crate::structs::User;
use sqlx::{pool::PoolConnection, Postgres};

pub fn create_token(user_id: i64, password: String) -> String {
    let signer = default_builder(password).build().into_timestamp_signer();

    signer.sign(general_purpose::URL_SAFE.encode(user_id.to_string()))
}

pub fn verify_token(token: String, user_id: String, password: String) -> Result<(), bool> {
    let signer = default_builder(password).build().into_timestamp_signer();

    let unsigned = signer.unsign(token.as_str());

    if let Ok(unsigned) = unsigned {
        let b64_user_id = unsigned.value().to_string();

        match general_purpose::URL_SAFE.decode(b64_user_id) {
            Ok(v) => {
                let value = std::str::from_utf8(v.as_slice()).unwrap();

                if value == user_id {
                    return Ok(());
                };
                Err(false)
            }
            Err(_) => Err(false),
        }
    } else {
        Err(false)
    }
}

pub async fn verify(token: String, mut db: PoolConnection<Postgres>) -> Result<User, &'static str> {
    let splits: Vec<&str> = token.split('.').collect();

    let user_id = splits.first();

    if let Some(user_id) = user_id {
        let uid = user_id.parse::<i64>();

        if let Ok(user_id) = uid {
            let user = sqlx::query!("SELECT * FROM users WHERE id = $1", user_id)
                .fetch_one(&mut db)
                .await;

            if let Ok(user) = user {
                if verify_token(token, user.id.to_string(), user.password).is_ok() {
                    Ok(User {
                        id: user.id.to_string(),
                        username: user.username,
                        discriminator: user.discriminator,
                        email: user.email,
                        flags: user.flags,
                        system: user.system,
                        suspended: user.suspended,
                    })
                } else {
                    Err("Invalid Token")
                }
            } else {
                Err("User ID does not exist in this instance.")
            }
        } else {
            Err("User ID is not a 64-bit integer.")
        }
    } else {
        Err("User ID not present in token.")
    }
}
