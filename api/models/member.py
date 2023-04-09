# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


import typing
from dataclasses import dataclass
from datetime import datetime

import asyncpg

from ..errors import CustomError
from ..metadata import Object, meta
from .user import User


@dataclass
class Member(Object):
    """Represents a Derailed Guild member."""

    user_id: int
    guild_id: int
    nick: str | None
    joined_at: datetime

    @classmethod
    async def acquire(cls, user_id: int, guild_id: int) -> typing.Self:
        """Acquire a member from a guild.

        Parameters
        ----------
        user_id: :class:`int`
            The user id of this member.
        guild_id: :class:`int`
            The Guild this user resides in.

        Raises
        ------
        CustomError: User '{user_id}' is not member of Guild
        """

        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "SELECT * FROM members WHERE user_id = $1 AND guild_id = $2;"
            )
            row = await stmt.fetchrow(user_id, guild_id)

            if row is None:
                raise CustomError(f"User '{user_id}' is not member of Guild")

            return cls(
                user_id=user_id,
                guild_id=guild_id,
                nick=row["nick"],
                joined_at=datetime.fromisoformat(row["joined_at"]),
            )

    @classmethod
    async def join(cls, user_id: int, guild_id: int) -> typing.Self:
        """Join this Guild as a user.

        Parameters
        ----------
        user_id: :class:`int`
            The user to be added.
        guild_id: :class:`int`
            The Guild whose receiving this member.
        """

        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "INSERT INTO members (user_id, guild_id, nick, joined_at)"
            )

            try:
                dt = datetime.utcnow()
                await stmt.fetch(user_id, guild_id, None, dt.isoformat())
            except asyncpg.UniqueViolationError:
                raise CustomError("User is already in Guild")

            return cls(user_id=user_id, guild_id=guild_id, nick=None, joined_at=dt)

    async def modify(self) -> None:
        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "UPDATE members SET nick = $3 WHERE user_id = $1 AND guild_id = $2;"
            )
            await stmt.fetch(self.user_id, self.guild_id, self.nick)

    async def publicize(self, secure: bool = False) -> dict[str, typing.Any]:
        if secure:
            return {
                "user": await (await User.acquire(self.user_id)).publicize(),
                "guild_id": self.guild_id,
                "nick": self.nick,
                "joined_at": self.joined_at,
            }
        else:
            return {
                "user_id": self.user_id,
                "guild_id": self.guild_id,
                "nick": self.nick,
                "joined_at": self.joined_at,
            }
