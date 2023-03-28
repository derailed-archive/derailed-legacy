/*
    SPDX-License-Identifier: AGPL-3.0
    Copyright 2021-2023 Derailed
*/

use crate::errors::DerailedError;
use crate::structs::User;
use actix_web::{post, web, Responder, Result};
use datar::State;
use serde::Deserialize;
use serde_valid::Validate;

#[derive(Deserialize, Debug, Validate)]
struct Register {
    #[validate(max_length = 32)]
    username: String,
    #[validate(max_length = 100)]
    email: String,
    #[validate(max_length = 74)]
    password: String,
}

#[post("/register")]
async fn register(state: web::Data<State>, data: web::Json<Register>) -> Result<impl Responder> {
    let password = bcrypt::hash(data.password, 18).unwrap();

    let db = state.db.acquire().await.unwrap();
    let user_id = state.sf.generate();
    let discriminator = sqlx::query!(
        "INSERT INTO users
            (id, username, email, password)
        VALUES
            ($1, $2, $3, $4)
        RETURNING
            discriminator",
        user_id,
        data.username,
        data.email,
        password
    )
    .fetch_optional(&mut db)
    .await?;

    if discriminator.is_none() {
        return Err((DerailedError::BadData {
            reason: "No discriminator available for username".to_string(),
        })
        .into());
    };

    return Ok(web::Json(User {
        id: user_id.to_string(),
        username: data.username,
        discriminator: discriminator,
        email: data.email,
        flags: 0,
        system: false,
        suspended: false,
    }));
}
