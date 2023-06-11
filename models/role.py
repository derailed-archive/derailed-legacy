# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


import typing
from dataclasses import dataclass

from ..api.errors import CustomError
from ..api.flags import RolePermissions
from ..api.metadata import Object, meta
from ..api.utils import MISSING, Maybe

ADMIN_PERM = RolePermissions.ADMINISTRATOR.value


@dataclass
class Role(Object):
    id: int
    guild_id: int
    name: str
    allow: RolePermissions
    deny: RolePermissions
    position: int

    def has_permission(self, perm: int | RolePermissions) -> bool:
        return self.has_permissions(perms=[perm])

    def has_permissions(self, perms: list[int | RolePermissions]) -> bool:
        results: list[bool] = []

        for perm in perms:
            if isinstance(perm, RolePermissions):
                perm = perm.value

            if bool(self.allow, ADMIN_PERM):
                results.append(True)
                continue

            # deny takes precedent over allow
            if bool(self.deny, perm) is True:
                results.append(False)
                continue
            elif bool(self.allow, perm) is True:
                results.append(True)
                continue
            else:
                results.append(False)
                continue

        if False in results:
            return False

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
    async def create(
        cls,
        name: str,
        guild_id: int,
        allow: int = 0,
        deny: int = 0,
        position: Maybe[int] = MISSING,
    ) -> typing.Self:
        async with meta.db.acquire() as db:
            role_id = meta.genflake()
            stmt = await db.prepare(
                "INSERT INTO guild_roles (id, name, guild_id, allow, deny, position) VALUES ($1, $3, $2, $4, $5, $6);"
            )
            await stmt.fetch(role_id, guild_id, name, allow, deny, position or 0)

            self = cls(
                id=role_id,
                name=name,
                guild_id=guild_id,
                allow=allow,
                deny=deny,
                position=position,
            )
            await self.move(position or 0)

            return self

    @classmethod
    async def acquire_all(cls, guild_id: int) -> list[typing.Self]:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("SELECT * FROM guild_roles WHERE guild_id = $1;")
            rows = await stmt.fetch(guild_id)

        roles: list[typing.Self] = []

        for row in rows:
            roles.append(
                cls(
                    id=id,
                    guild_id=row["guild_id"],
                    name=row["name"],
                    allow=RolePermissions(row["allow"]),
                    deny=RolePermissions(row["deny"]),
                    position=row["position"],
                )
            )

        return roles

    async def publicize(self, secure: bool = False) -> dict[str, typing.Any]:
        return {
            "id": str(self.id),
            "guild_id": str(self.guild_id),
            "name": self.name,
            "allow": str(self.allow),
            "deny": str(self.deny),
            "position": self.position,
        }

    async def move(self, position: int) -> None:
        if position == self.position:
            return

        roles = await Role.acquire_all(self.guild_id)

        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "UPDATE guild_roles SET position = $2 WHERE id = $1;"
            )

            updates: dict[int, int] = {}

            for role in roles:
                if role.id == self.id:
                    continue
                elif role.position >= self.position:
                    updates[role.id] = role.position + 1
                elif role.position <= self.position:
                    updates[role.id] = role.position - 1

            if updates == {}:
                return

            await stmt.executemany([(rid, rp) for rid, rp in updates.items()])

            self.position = position

    async def modify(self) -> None:
        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "UPDATE guild_roles SET name = $2, allow = $3, deny = $4, position = $5 WHERE id = $1"
            )

            await stmt.fetch(
                self.id, self.name, self.allow.value, self.deny.value, self.position
            )

    async def delete(self) -> None:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("DELETE FROM guild_roles WHERE id = $1;")
            await stmt.fetchrow(self.id)
