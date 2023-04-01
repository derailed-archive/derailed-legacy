/*
    SPDX-License-Identifier: AGPL-3.0
    Copyright 2021-2023 Derailed
*/

use crate::errors::verify_idiomatic;
use actix_web::{get, http::header::HeaderValue, web, Responder, Result};
use datar::State;
use tokio::sync::Mutex;

#[get("/users/@me")]
async fn get_me(
    req: actix_web::HttpRequest,
    state: web::Data<Mutex<State>>,
) -> Result<impl Responder> {
    let user = verify_idiomatic(
        req.headers()
            .get("authorization")
            .unwrap_or(&HeaderValue::from_static("authorization=0"))
            .to_str()
            .unwrap_or("")
            .to_string(),
        state.lock().await.db.acquire().await.unwrap(),
    )
    .await?;

    Ok(web::Json(user))
}
