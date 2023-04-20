"""Base

Revision ID: 3281dc6f9c24
Revises: 
Create Date: 2023-04-02 17:20:56.152075

Revision for the Derailed project, and protected under AGPL-3.0.
Copyright 2021-2023 Derailed
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "3281dc6f9c24"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """CREATE OR REPLACE FUNCTION generate_discriminator(TEXT)
    RETURNS TEXT
    LANGUAGE plpgsql
    AS $$
    DECLARE
        out VARCHAR(4);
    BEGIN
        SELECT * FROM (
            SELECT
                LPAD(CAST(trunc(random() * 9999 + 1) AS TEXT), 4, '0') AS discrim
            FROM
                generate_series(1, 9999)
        ) AS result
        WHERE result.discrim NOT IN (
            SELECT discriminator FROM users WHERE username = $1
        )
        LIMIT 1
        INTO out;
        RETURN substr(out, 1, 4);
    END;
    $$;"""
    )
    op.execute(
        """CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    CREATE OR REPLACE FUNCTION generate_invite_id()
    RETURNS TEXT
    LANGUAGE plpgsql
    AS $$
    DECLARE
        out TEXT;
    BEGIN
        SELECT * FROM (
            SELECT
                replace(replace(encode(gen_random_bytes(6), 'base64'), '/', '_'), '+', '-') AS invite_id
            FROM
                generate_series(1, 9999)
        ) AS result
        WHERE result.invite_id NOT IN (
            SELECT id FROM invites WHERE id = $1
        )
        LIMIT 1
        INTO out;
        RETURN out;
    END;
    $$;"""
    )

    op.create_table(
        "users",
        sa.Column("id", sa.BIGINT, primary_key=True),
        sa.Column("username", sa.VARCHAR(32), nullable=False, index=True),
        sa.Column(
            "discriminator",
            sa.TEXT,
            nullable=False,
            server_default=sa.func.generate_discriminator("username"),
        ),
        sa.Column("email", sa.VARCHAR(100), nullable=False, unique=True, index=True),
        sa.Column("password", sa.TEXT, nullable=False),
        sa.Column("flags", sa.INT, nullable=False, server_default="0"),
        sa.Column("system", sa.BOOLEAN, server_default="FALSE"),
        sa.Column("deletor_job_id", sa.BIGINT, unique=True),
        sa.Column("suspended", sa.BOOLEAN, server_default="FALSE"),
    )

    op.create_table(
        "user_settings",
        sa.Column("user_id", sa.BIGINT, sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("status", sa.INT),
        sa.Column("theme", sa.TEXT),
    )

    op.create_table(
        "guilds",
        sa.Column("id", sa.BIGINT, primary_key=True),
        sa.Column("name", sa.VARCHAR(32)),
        sa.Column("flags", sa.INT, nullable=False, server_default="0"),
        sa.Column(
            "owner_id",
            sa.BIGINT,
            sa.ForeignKey("users.id", ondelete="NO ACTION"),
            nullable=False,
        ),
        sa.Column("permissions", sa.BIGINT, nullable=False),
    )

    op.create_table(
        "channels",
        sa.Column("id", sa.BIGINT, primary_key=True),
        sa.Column("name", sa.VARCHAR(32)),
        sa.Column("type", sa.INT, nullable=False),
        sa.Column(
            "guild_id", sa.BIGINT, sa.ForeignKey("guilds.id", ondelete="CASCADE")
        ),
        sa.Column("last_message_id", sa.BIGINT),
        sa.Column(
            "parent_id", sa.BIGINT, sa.ForeignKey("channels.id", ondelete="SET NULL")
        ),
        sa.Column("position", sa.INT),
    )

    op.create_table(
        "invites",
        sa.Column("id", sa.TEXT, primary_key=True),
        sa.Column(
            "guild_id",
            sa.BIGINT,
            sa.ForeignKey("guilds.id", ondelete="CASCADE"),
            index=True,
            nullable=False,
        ),
        sa.Column(
            "author_id", sa.BIGINT, sa.ForeignKey("users.id", ondelete="SET NULL")
        ),
        sa.Column(
            "channel_id",
            sa.BIGINT,
            sa.ForeignKey("channels.id", ondelete="CASCADE"),
            index=True,
            nullable=False,
        ),
        sa.Column("created_at", sa.DATE, server_default=sa.func.now()),
    )

    op.create_table(
        "user_guild_positions",
        sa.Column(
            "user_id",
            sa.BIGINT,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "guild_id",
            sa.BIGINT,
            sa.ForeignKey("guilds.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("position", sa.INT, nullable=False),
    )

    op.create_table(
        "activities",
        sa.Column("id", sa.BIGINT, primary_key=True),
        sa.Column(
            "user_id",
            sa.BIGINT,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("type", sa.INT, nullable=False),
        sa.Column("created_at", sa.DATE, nullable=False),
        sa.Column("content", sa.VARCHAR(32)),
    )

    op.create_table(
        "members",
        sa.Column(
            "user_id",
            sa.BIGINT,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "guild_id",
            sa.BIGINT,
            sa.ForeignKey("guilds.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("nick", sa.VARCHAR(32)),
        sa.Column("joined_at", sa.DATE, server_default=sa.func.now()),
    )

    op.create_table(
        "guild_roles",
        sa.Column("id", sa.BIGINT, primary_key=True),
        sa.Column(
            "guild_id",
            sa.BIGINT,
            sa.ForeignKey("guilds.id", ondelete="CASCADE"),
            index=True,
            nullable=False,
        ),
        sa.Column("name", sa.VARCHAR(32), nullable=False),
        sa.Column("allow", sa.BIGINT, nullable=False),
        sa.Column("deny", sa.BIGINT, nullable=False),
        sa.Column("position", sa.INT, nullable=False),
    )

    op.create_table(
        "member_assigned_roles",
        sa.Column(
            "role_id", sa.BIGINT, sa.ForeignKey("guild_roles.id", ondelete="CASCADE"), primary_key=True
        ),
        sa.Column(
            "guild_id", sa.BIGINT, sa.ForeignKey("guilds.id", ondelete="CASCADE")
        ),
        sa.Column("user_id", sa.BIGINT, sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "messages",
        sa.Column("id", sa.BIGINT, primary_key=True),
        sa.Column(
            "channel_id",
            sa.BIGINT,
            sa.ForeignKey("channels.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "author_id", sa.BIGINT, sa.ForeignKey("users.id", ondelete="SET NULL")
        ),
        sa.Column("content", sa.VARCHAR(2048)),
        sa.Column("timestamp", sa.DATE, nullable=False),
        sa.Column("edited_timestamp", sa.DATE),
    )

    op.create_table(
        "read_states",
        sa.Column(
            "channel_id",
            sa.BIGINT,
            sa.ForeignKey("channels.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "user_id",
            sa.BIGINT,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("last_message_id", sa.BIGINT),
    )


def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS generate_discriminator(TEXT);")
    op.drop_table("users")
    op.drop_table("user_settings")
    op.drop_table("guilds")
    op.drop_table("channels")
    op.drop_table("invites")
    op.drop_table("user_guild_positions")
    op.drop_table("activities")
    op.drop_table("members")
    op.drop_table("guild_roles")
    op.drop_table("member_assigned_roles")
    op.drop_table("messages")
    op.drop_table("read_states")
