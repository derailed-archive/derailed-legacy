CREATE OR REPLACE FUNCTION generate_discriminator(TEXT)
RETURNS SMALLINT
LANGUAGE plpgsql
AS $$
DECLARE
    out SMALLINT;
BEGIN
    SELECT * FROM (
        SELECT
            trunc(random() * 9999 + 1) AS discrim
        FROM
            generate_series(1, 9999)
    ) AS result
    WHERE result.discrim NOT IN (
        SELECT discriminator FROM users WHERE username = $1
    )
    LIMIT 1
    INTO out;
    RETURN out;
END;
$$;

CREATE TABLE IF NOT EXISTS users (
    id bigint PRIMARY KEY,
    username varchar(32) NOT NULL,
    discriminator varchar(4) NOT NULL DEFAULT generate_discriminator('username'),
    email varchar(100) NOT NULL UNIQUE,
    password text NOT NULL,
    flags int NOT NULL DEFAULT 0,
    system boolean NOT NULL DEFAULT false,
    deletor_job_id bigint UNIQUE,
    suspended boolean NOT NULL DEFAULT false
);

CREATE UNIQUE INDEX user_email ON users (email);
CREATE INDEX usernames ON users (username);

CREATE TABLE IF NOT EXISTS user_settings (
    user_id bigint PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    status int
);

CREATE TABLE IF NOT EXISTS guilds (
    id bigint PRIMARY KEY,
    name varchar(32) NOT NULL,
    flags int NOT NULL,
    owner_id bigint REFERENCES users(id) ON DELETE NO ACTION,
    permissions bigint NOT NULL
);

CREATE TABLE IF NOT EXISTS channels (
    id bigint PRIMARY KEY,
    type int NOT NULL,
    name varchar(32),
    last_message_id bigint,
    parent_id bigint REFERENCES channels(id) ON DELETE SET NULL,
    guild_id bigint REFERENCES guilds(id) ON DELETE CASCADE,
    position int
);

CREATE TABLE IF NOT EXISTS invites (
    id text PRIMARY KEY,
    guild_id bigint NOT NULL REFERENCES guilds(id) ON DELETE CASCADE,
    author_id bigint NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    channel_id bigint NOT NULL REFERENCES channels(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS user_guild_positions (
    user_id bigint NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    guild_id bigint NOT NULL REFERENCES guilds(id) ON DELETE CASCADE,
    position int NOT NULL
);

CREATE TABLE IF NOT EXISTS activities (
    id bigint PRIMARY KEY,
    user_id bigint NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type int,
    created_at text,
    content varchar(32)
);

CREATE TABLE IF NOT EXISTS members (
    user_id bigint NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    guild_id bigint NOT NULL REFERENCES guilds(id) ON DELETE CASCADE,
    nick varchar(32),
    PRIMARY KEY (user_id, guild_id)
);

CREATE TABLE IF NOT EXISTS guild_roles (
    id bigint PRIMARY KEY,
    guild_id bigint NOT NULL REFERENCES guilds(id) ON DELETE CASCADE,
    name varchar(32),
    allow_permissions bigint NOT NULL,
    deny_permissions bigint NOT NULL,
    position int
);

CREATE TABLE IF NOT EXISTS member_assigned_roles (
    role_id bigint NOT NULL REFERENCES guild_roles(id) ON DELETE CASCADE,
    user_id bigint NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

-- These tables will eventually be migrated in favor for ScyllaDB

CREATE TABLE IF NOT EXISTS messages (
    id bigint PRIMARY KEY,
    channel_id bigint NOT NULL REFERENCES channels(id) ON DELETE CASCADE,
    author_id bigint NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content varchar(2048) NOT NULL,
    timestamp time NOT NULL,
    edited_timestamp time
);

CREATE TABLE IF NOT EXISTS read_states (
    user_id bigint NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    channel_id bigint NOT NULL REFERENCES channels(id) ON DELETE CASCADE,
    last_message_id bigint
);
