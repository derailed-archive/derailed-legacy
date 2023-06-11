# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


import datetime
import typing
from dataclasses import dataclass

from ..errors import CustomError
from ..metadata import Object, meta
from ..utils import MISSING, Maybe
from .channel import Channel
from .guild import Guild
from .user import User


@dataclass
class Invite(Object):
    id: str
    guild_id: int
    author_id: int
    channel_id: int
    created_at: datetime.datetime

    async def publicize(
        self,
        secure: bool = False,
        guild: Maybe[Guild] = MISSING,
        author: Maybe[User] = MISSING,
        channel: Maybe[Channel] = MISSING,
    ) -> dict[str, typing.Any]:
        if not guild:
            guild = await Guild.acquire(self.guild_id)

        if not author:
            author = await User.acquire(self.author_id)

        if not channel:
            channel = await Channel.acquire(self.channel_id)

        return {
            "id": self.id,
            "guild": guild.publicize(),
            "author": author.partialize("id", "username"),
            "channel": channel.partialize("id", "name"),
            "created_at": self.created_at,
        }

    @classmethod
    async def create(
        cls, guild_id: int, author_id: int, channel_id: int, created_at: str
    ) -> typing.Self:
        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "INSERT INTO invites (guild_id, author_id, channel_id, created_at) VALUES ($1, $2, $3, $4) RETURNING id;"
            )

            id = await stmt.fetchval(guild_id, author_id, channel_id, created_at)

            return cls(
                id=id,
                guild_id=guild_id,
                author_id=author_id,
                channel_id=channel_id,
                created_at=datetime.datetime.fromisoformat(created_at),
            )

    @classmethod
    async def acquire(cls, id: str) -> typing.Self:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("SELECT * FROM invites WHERE id = $1;")

            invite_row = await stmt.fetchrow(id)

            if invite_row is None:
                raise CustomError("Invite does not exist", 404)

            return cls(
                id=invite_row["id"],
                guild_id=invite_row["guild_id"],
                author_id=invite_row["author_id"],
                channel_id=invite_row["channel_id"],
                created_at=datetime.datetime.fromisoformat(invite_row["created_at"]),
            )

    async def delete(self) -> None:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("DELETE FROM invites WHERE id = $1;")

            await stmt.fetch(self.id)
