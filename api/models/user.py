# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

import typing
from dataclasses import dataclass

from ..errors import UserDoesNotExist, UsernameOverused
from ..metadata import Object, meta


@dataclass
class User(Object):
    """Represents a Derailed user."""

    id: int
    username: str
    discriminator: str
    email: str
    flags: int
    system: bool
    suspended: bool

    # private fields
    password: str | None = None
    deletor_job_id: int | None = None

    @classmethod
    async def register(
        self,
        user_id: int,
        username: str,
        email: str,
        password: str,
        system: bool = False,
    ) -> typing.Self:
        """Register a new user into Derailed.

        Parameters
        ----------
        user_id: :class:`int`
            A snowflake id to assign this user.
        username: :class:`str`
            The username to assign this user.
        email: :class:`str`
            A unique email for this user.
        password: :class:`str`
            The hashed password for securing this user's identity.
        system: :class:`bool`
            Whether this user is for Derailed's system.
            Defaults to `False`.
        """

        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                """INSERT INTO users
            (id, username, email, password, system)
        VALUES
            ($1, $2, $3, $4, $5)
        RETURNING
            discriminator""",
                name="register_user",
            )

            rec = await stmt.fetchrow(user_id, username, email, password, system)

            if rec is None:
                raise UsernameOverused

            user = User(
                id=user_id,
                username=username,
                discriminator=rec["discriminator"],
                email=email,
                flags=0,
                system=system,
                suspended=False,
                password=password,
            )
            user._cache()
            return user

    @classmethod
    async def acquire(self, user_id: int) -> typing.Self:
        """Acquire a user using their ID.

        Parameters
        ----------
        user_id: :class:`int`
            The user id to acquire

        Raises
        ------
        UserDoesNotExist:
            Raised when no users with `user_id` exist.
        """

        obj = meta.cache.get(user_id)

        if obj:
            return obj

        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                f"SELECT * FROM users WHERE id = $1;", name="select_user_id"
            )
            user_row = await stmt.fetchrow(user_id)

            if user_row is None:
                raise UserDoesNotExist

            user = User(**dict(user_row))
            user._cache()
            return user

    async def publicize(self, secure: bool = False) -> dict[str, typing.Any]:
        base = {
            "id": self.id,
            "username": self.username,
            "discriminator": self.discriminator,
            "flags": self.flags,
            "system": self.system,
            "suspended": self.suspended,
        }

        if secure:
            base["email"] = self.email

        return base

    def _cache(self) -> None:
        meta.cache[self.id] = self
