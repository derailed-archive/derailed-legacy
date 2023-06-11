# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


import typing
from dataclasses import dataclass

from ..api.errors import UserDoesNotExist
from ..api.metadata import Object, meta


@dataclass
class Settings(Object):
    """Represents a users' settings."""

    user_id: int
    theme: str
    status: int

    @classmethod
    async def acquire(cls, user_id: int) -> typing.Self:
        """Acquire the settings of a user.

        Parameters
        ----------
        user_id: :class:`int`
            The user whose settings to acquire.
        """

        async with meta.db.acquire() as db:
            stmt = await db.prepare("SELECT * FROM user_settings WHERE user_id = $1;")
            row = await stmt.fetchrow(user_id)
            if row is None:
                raise UserDoesNotExist

            return cls(**dict(row))

    async def modify(self) -> None:
        """Modify the properties of this users' settings."""

        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                f"UPDATE user_settings SET theme = $2, status = $3 WHERE user_id = $1;"
            )
            await stmt.fetch(self.user_id, self.theme, self.status)

    async def publicize(self, secure: bool = False) -> dict[str, typing.Any]:
        return {"theme": self.theme, "status": self.status}
