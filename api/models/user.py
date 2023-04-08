# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

import typing
from dataclasses import dataclass

import asyncpg

from ..errors import CustomError, UserDoesNotExist, UsernameOverused
from ..metadata import Object, meta
from .settings import Settings


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

    async def get_settings(self) -> Settings:
        return Settings.acquire(self.id)

    @classmethod
    async def register(
        cls,
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
                """INSERT INTO users (id, username, email, password, system) VALUES ($1, $2, $3, $4, $5) RETURNING discriminator;""",
            )

            try:
                rec = await stmt.fetchrow(user_id, username, email, password, system)
            except asyncpg.UniqueViolationError:
                raise CustomError("Email already used")

            if rec is None:
                raise UsernameOverused

            user = cls(
                id=user_id,
                username=username,
                discriminator=rec["discriminator"],
                email=email,
                flags=0,
                system=system,
                suspended=False,
                password=password,
            )
            return user

    @classmethod
    async def acquire(self, user_id: int) -> typing.Self:
        """Acquire a user using their ID.

        Parameters
        ----------
        user_id: :class:`int`
            The user id to acquire.

        Raises
        ------
        UserDoesNotExist:
            Raised when no users with `user_id` exist.
        """
        async with meta.db.acquire() as db:
            stmt = await db.prepare(f"SELECT * FROM users WHERE id = $1;")
            user_row = await stmt.fetchrow(user_id)

            if user_row is None:
                raise UserDoesNotExist

            user = User(**dict(user_row))
            return user

    async def publicize(self, secure: bool = False) -> dict[str, typing.Any]:
        base = {
            "id": str(self.id),
            "username": self.username,
            "discriminator": self.discriminator,
            "flags": self.flags,
            "system": self.system,
            "suspended": self.suspended,
        }

        if secure:
            base["email"] = self.email

        return base

    async def modify(self) -> None:
        if self == self.___old_self:
            return

        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "UPDATE users SET username = $1, discriminator = $2, flags = $3, suspended = $4, email = $5, password = $6 WHERE id = $7;",
            )
            await stmt.fetch(
                self.username,
                self.discriminator,
                self.flags,
                self.suspended,
                self.email,
                self.password,
                self.id,
            )

    async def delete(self) -> None:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("DELETE FROM users WHERE id = $1;")
            try:
                await stmt.fetchrow(self.id)
            except asyncpg.TriggeredActionError:
                raise CustomError("Cannot delete user due to a continuous dependency")

    def __eq__(self, value: "User") -> bool:
        return (
            self.username == value.username
            and self.discriminator == value.discriminator
            and self.flags == value.flags
            and self.suspended == value.suspended
            and self.email == value.email
            and self.password == value.password
        )
