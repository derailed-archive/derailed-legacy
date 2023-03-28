/*
    SPDX-License-Identifier: AGPL-3.0
    Copyright 2021-2023 Derailed
*/

use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct User {
    pub id: String,
    pub username: String,
    pub discriminator: String,
    pub email: String,
    pub flags: i32,
    pub system: bool,
    pub suspended: bool,
}
