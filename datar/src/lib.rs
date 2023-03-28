/*
    SPDX-License-Identifier: AGPL-3.0
    Copyright 2021-2023 Derailed
*/

use sqlx::{postgres::PgPoolOptions, PgPool};

#[derive(Debug)]
pub struct State {
    pub db: PgPool,
}

pub async fn create_pool(uri: &str) -> Result<PgPool, sqlx::Error> {
    PgPoolOptions::new().connect(uri).await
}

pub async fn migrate(pool: &PgPool) {
    sqlx::migrate!("../migrations").run(pool).await.unwrap()
}
