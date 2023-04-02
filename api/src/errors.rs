/*
    SPDX-License-Identifier: AGPL-3.0
    Copyright 2021-2023 Derailed
*/

use actix_web::{error, http::{StatusCode, header::HeaderValue}, HttpResponse};
use datar::{auth::verify, structs::User};
use derive_more::{Display, Error};
use sqlx::{pool::PoolConnection, Postgres};

#[derive(Debug, Display, Error)]
pub enum DerailedError {
    InternalError,
    BadData,
    Timeout,
    Unauthorized,
    Forbidden,
}

pub async fn verify_idiomatic(
    req: actix_web::HttpRequest,
    db: PoolConnection<Postgres>,
) -> actix_web::Result<User> {
    let token = req.headers()
        .get("authorization")
        .unwrap_or(&HeaderValue::from_static("null"))
        .to_str()
        .unwrap_or("")
        .to_string();

    if let Ok(user) = verify(token, db).await {
        Ok(user)
    } else {
        Err((DerailedError::Unauthorized).into())
    }
}

impl error::ResponseError for DerailedError {
    fn error_response(&self) -> HttpResponse {
        HttpResponse::build(self.status_code()).finish()
    }

    fn status_code(&self) -> StatusCode {
        match *self {
            DerailedError::InternalError => StatusCode::INTERNAL_SERVER_ERROR,
            DerailedError::BadData => StatusCode::BAD_REQUEST,
            DerailedError::Timeout => StatusCode::GATEWAY_TIMEOUT,
            DerailedError::Forbidden => StatusCode::FORBIDDEN,
            DerailedError::Unauthorized => StatusCode::UNAUTHORIZED,
        }
    }
}
