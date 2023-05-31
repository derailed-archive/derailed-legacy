# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


import typing
from dataclasses import dataclass
from datetime import datetime

import asyncpg

from ..errors import CustomError
from ..flags import RolePermissions
from ..metadata import Object, meta
from ..utils import cache
from .guild import Guild
from .role import ADMIN_PERM, Role
from .user import User


@dataclass
class Member(Object):
    """Represents a Derailed Guild member."""

    user_id: int
    guild_id: int
    nick: str | None
    joined_at: datetime

    async def highest_role_position(self) -> int:
        roles = await self.get_roles()
        role_positions = [role.position for role in roles]

        return max(role_positions)

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
                "INSERT INTO members (user_id, guild_id, nick, joined_at) VALUES ($1, $2, $3, $4);"
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

    @cache()
    async def get_roles(self) -> list[Role]:
        """Fetches the roles for this Member."""

        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "SELECT * FROM roles WHERE id IN "
                "(SELECT id FROM member_assigned_roles "
                "WHERE user_id = $1 AND guild_id = $2);"
            )
            rows = await stmt.fetch(self.user_id, self.guild_id)

        roles = []

        for row in rows:
            roles.insert(
                row["position"],
                Role(
                    id=row["id"],
                    guild_id=row["guild_id"],
                    name=row["name"],
                    allow=RolePermissions(row["allow"]),
                    deny=RolePermissions(row["deny"]),
                    position=row["position"],
                ),
            )

        return roles

    async def has_permissions(
        self, perms: list[int | RolePermissions], guild: Guild | None = None
    ) -> None:
        roles = await self.get_roles()

        if roles != []:
            for role in roles:
                if not role.has_permissions(perms=perms):
                    raise CustomError("Need elevated permissions to do action", 403)
        else:
            if guild:
                for perm in perms:
                    if bool(guild.permissions & ADMIN_PERM) is True:
                        break

                    if not bool(guild.permissions & perm):
                        raise CustomError("Need elevated permissions to do action", 403)
