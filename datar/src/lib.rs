/*
    SPDX-License-Identifier: AGPL-3.0
    Copyright 2021-2023 Derailed
*/

use sqlx::{postgres::PgPoolOptions, PgPool};
use chrono::Utc;
pub mod structs;

#[derive(Debug, Clone)]
pub struct Snowflake {
    epoch: i64,
    thread_id: i64,
    process_id: i64,
    sequence: i64,
}


// Snowflake implementation
impl Snowflake {
    pub fn new(epoch: i64, thread_id: i64, process_id: i64) -> Snowflake {
        Snowflake {
            epoch,
            thread_id,
            process_id,
            sequence: 0,
        }
    }

    pub fn generate(&mut self) -> i64 {
        let timestamp = self.get_time();
        self.sequence = self.sequence + 1;

        return (timestamp << 22) | (self.thread_id << 17) | (self.process_id << 12) | self.sequence
    }

    fn get_time(&self) -> i64 {
        Utc::now().timestamp_millis() - self.epoch
    }
}
#[derive(Debug, Clone)]
pub struct State {
    pub db: PgPool,
    pub sf: Snowflake
}


pub async fn create_pool(uri: &str) -> Result<PgPool, sqlx::Error> {
    PgPoolOptions::new().connect(uri).await
}

pub async fn migrate(pool: &PgPool) {
    sqlx::migrate!("../migrations").run(pool).await.unwrap()
}
