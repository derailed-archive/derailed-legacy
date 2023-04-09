# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


import typing
from dataclasses import dataclass

from ..utils import MISSING, Maybe

from ..errors import CustomError
from ..flags import RolePermissions
from ..metadata import Object, meta


@dataclass
class Role(Object):
    id: int
    guild_id: int
    name: str
    allow: RolePermissions
    deny: RolePermissions
    position: int

    @classmethod
    async def acquire(cls, id: int) -> typing.Self:
        """Acquire a role in a Guild.

        Parameters
        ----------
        id: :class:`int`
            The role to acquire.
        """

        async with meta.db.acquire() as db:
            stmt = await db.prepare("SELECT * FROM guild_roles WHERE id = $1;")
            row = await stmt.fetchrow(id)

            if row is None:
                raise CustomError("Role does not exist in any Guild")

            return cls(
                id=id,
                guild_id=row["guild_id"],
                name=row["name"],
                allow=RolePermissions(row["allow"]),
                deny=RolePermissions(row["deny"]),
                position=row["position"],
            )

    @classmethod
    async def create(cls, name: str, guild_id: int, allow: int = 0, deny: int = 0, position: Maybe[int | None] = MISSING) -> typing.Self:
        if position is None:
            position = 0

        # TODO!

    async def publicize(self, secure: bool = False) -> dict[str, typing.Any]:
        return {
            "id": str(self.id),
            "guild_id": str(self.guild_id),
            "name": self.name,
            "allow": str(self.allow),
            "deny": str(self.deny),
            "position": self.position,
        }
