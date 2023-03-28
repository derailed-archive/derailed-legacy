/*
    SPDX-License-Identifier: AGPL-3.0
    Copyright 2021-2023 Derailed
*/

use actix_web::{web, App, HttpServer};
use dotenvy::dotenv;
use std::env;
use std::process;
use std::sync::Arc;
pub mod errors;
mod routes;
pub mod structs;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenv().ok();
    let db = datar::create_pool(env::var("PG_URI").unwrap().as_str())
        .await
        .unwrap();
    datar::migrate(&db).await;
    let sf = datar::Snowflake::new(
        1672531200000,
        thread_id::get().try_into().unwrap(),
        process::id().try_into().unwrap(),
    );
    let state = Arc::new(datar::State { db, sf });

    HttpServer::new(move || App::new().app_data(web::Data::new(state.clone())))
        .bind(("0.0.0.0", 8080))?
        .run()
        .await
}
