/*
    SPDX-License-Identifier: AGPL-3.0
    Copyright 2021-2023 Derailed
*/

use actix_web::{
    error,
    http::{header::ContentType, StatusCode},
    HttpResponse,
};
use derive_more::{Display, Error};

#[derive(Debug, Display, Error)]
pub enum DerailedError {
    #[display(fmt = "Internal Server Error")]
    InternalError,
    BadData {
        reason: String,
    },

    #[display(fmt = "Gateway Timeout")]
    Timeout,
}

impl error::ResponseError for DerailedError {
    fn error_response(&self) -> HttpResponse {
        HttpResponse::build(self.status_code())
            .insert_header(ContentType::plaintext())
            .body(self.to_string())
    }

    fn status_code(&self) -> StatusCode {
        match *self {
            DerailedError::InternalError => StatusCode::INTERNAL_SERVER_ERROR,
            DerailedError::BadData { reason } => StatusCode::BAD_REQUEST,
            DerailedError::Timeout => StatusCode::GATEWAY_TIMEOUT,
        }
    }
}
