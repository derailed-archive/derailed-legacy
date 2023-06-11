# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


import datetime
import typing
from dataclasses import dataclass

from asyncpg import Record

from ..api.errors import GuildDoesNotExist
from ..api.flags import DEFAULT_PERMISSIONS, RolePermissions
from ..api.metadata import Object, meta
from ..api.utils import cache
from .channel import Channel


@dataclass
class Guild(Object):
    """Represents a Derailed Guild."""

    id: int
    name: str
    flags: int
    owner_id: int
    permissions: RolePermissions

    @classmethod
    async def acquire(cls, id: int) -> typing.Self:
        """Acquire this Guild from the database via its ID.

        Parameters
        ----------
        id: :class:`int`
            The ID of the Guild to fetch.

        Raises
        ------
        GuildDoesNotExist:
            No Guild with this ID exists.
        """

        async with meta.db.acquire() as db:
            stmt = await db.prepare("SELECT * FROM guilds WHERE id = $1;")
            rec = await stmt.fetchrow(id)

            if rec is None:
                raise GuildDoesNotExist

            permissions = RolePermissions(rec["permissions"])
            return cls(
                id=rec["id"],
                name=rec["name"],
                flags=rec["flags"],
                owner_id=rec["owner_id"],
                permissions=permissions,
            )

    @classmethod
    async def create(
        cls,
        name: str,
        owner_id: int,
        flags: int = 0,
        permissions: RolePermissions = DEFAULT_PERMISSIONS,
    ) -> typing.Self:
        """Creates a new Guild.

        Parameters
        ----------
        name: :class:`str`
            The name of this Guild.
        owner_id: :class:`int`
            The Guild's owner id.
        flags: :class:`int`
            The flags to give this Guild.
            Defaults to 0.
        permissions: :class:`RolePermissions`
            The permissions to give this Guild.
            Defaults to a normalized permissions number.
        """

        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "INSERT INTO guilds (id, name, owner_id, flags, "
                "permissions) VALUES ($1, $2, $3, $4, $5);"
            )
            stmt2 = await db.prepare(
                "INSERT INTO members (user_id, guild_id, nick, "
                "joined_at) VALUES ($1, $2, $3, $4);"
            )
            stmt3 = await db.prepare(
                "INSERT INTO channels (id, name, type, guild_id, "
                "parent_id, position) VALUES ($1, $2, $3, $4, $5, $6);"
            )
            guild_id = meta.genflake()
            trans = db.transaction()
            await trans.start()

            try:
                await stmt.fetch(guild_id, name, owner_id, flags, int(permissions))
                await stmt2.fetch(
                    owner_id, guild_id, None, datetime.datetime.utcnow().isoformat()
                )
                cat = meta.genflake()
                await stmt3.fetch(cat, "General", 0, guild_id, None, 0)
                await stmt3.fetch(meta.genflake(), "general", 1, guild_id, cat, 0)
            except Exception as exc:
                await trans.rollback()
                raise exc

            await trans.commit()

            return cls(
                id=guild_id,
                name=name,
                flags=flags,
                owner_id=owner_id,
                permissions=permissions,
            )

    async def modify(self) -> None:
        """Modifies an active Guild to propose new properties."""

        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "UPDATE guilds SET name = $2, owner_id = $3, flags = $4, permissions = $5 WHERE id = $1"
            )
            await stmt.fetch(
                self.id, self.name, self.owner_id, self.flags, int(self.permissions)
            )

    async def delete(self) -> None:
        """Deletes this Guild, and its children (members, channels, etc.) from the database."""

        async with meta.db.acquire() as db:
            stmt = await db.prepare("DELETE FROM guilds WHERE id = $1;")
            await stmt.fetch(self.id)

    async def publicize(self, secure: bool = False) -> dict[str, typing.Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "flags": self.flags,
            "owner_id": str(self.owner_id),
            "permissions": str(self.permissions),
        }

    def _form_channel(
        self, row: Record | None, rows: list[Record] = []
    ) -> Channel | None:
        if row is None:
            return None

        return Channel(
            id=row["id"],
            name=row["name"],
            type=row["type"],
            guild_id=self.id,
            last_message_id=row["last_message_id"],
            parent=self._form_channel(rows.get(row["parent_id"]), rows),
            position=row["position"],
        )

    @cache()
    async def get_channels(self) -> list[Channel]:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("SELECT * FROM channels WHERE guild_id = $1;")

            raw_rows = await stmt.fetch(self.id)

            rows = {r["id"]: r for r in raw_rows}

        channels = []

        for row in rows:
            channels.append(self._form_channel(row, rows))

        return channels

    async def highest_channel_position(self) -> int:
        channels = await self.get_channels()
        channel_positions = [channel.position for channel in channels]

        return max(channel_positions)
