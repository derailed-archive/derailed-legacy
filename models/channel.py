# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

from __future__ import annotations

import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from .guild import Guild

from ..api.errors import CustomError
from ..api.metadata import Object, meta


@dataclass
class Channel(Object):
    id: int
    name: str
    type: int
    guild_id: int | None
    last_message_id: int | None
    parent: Channel | None
    position: int | None

    @property
    def parent_id(self) -> int | None:
        if self.parent:
            return self.parent.id
        else:
            return None

    async def publicize(self, secure: bool = False):
        return {
            "id": str(self.id),
            "name": self.name,
            "type": self.type,
            "guild_id": str(self.guild_id),
            "last_message_id": str(self.last_message_id),
            "parent_id": str(self.parent_id),
            "position": self.position,
        }

    @classmethod
    async def acquire_all(cls, guild_id: int) -> list[typing.Self]:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("SELECT * FROM channels WHERE guild_id = $1;")

            rows = await stmt.fetch(guild_id)

        acqs = []

        for row in rows:
            channel_id = row["id"]
            if row.get("parent_id") is not None:
                parent = await Channel.acquire(row["parent_id"])
            else:
                parent = None

            acqs.append(cls(
                id=channel_id,
                name=row["name"],
                type=row["type"],
                guild_id=row.get("guild_id"),
                last_message_id=row.get("last_message_id"),
                parent=parent,
                position=row.get("position"),
            ))

        return acqs

    @classmethod
    async def acquire(cls, channel_id: int) -> typing.Self:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("SELECT * FROM channels WHERE id = $1;")

            row = await stmt.fetchrow(channel_id)

            if row is None:
                raise CustomError("Channel does not exist")

            if row.get("parent_id") is not None:
                parent = await Channel.acquire(row["parent_id"])
            else:
                parent = None

            return cls(
                id=channel_id,
                name=row["name"],
                type=row["type"],
                guild_id=row.get("guild_id"),
                last_message_id=row.get("last_message_id"),
                parent=parent,
                position=row.get("position"),
            )

    def __mover(self, db, ep_stmt, hp):
        ret = ()
        for i in range(hp):
            if i >= self.position:
                ret.append((i, i + 1))
            else:
                ret.append((i, i - 1))

        return ret

    async def move(self, guild: Guild) -> None:
        async with meta.db.acquire() as db:
            hp_stmt = await db.prepare(
                f"SELECT max(position) FROM channels WHERE guild_id = $1 AND parent_id = $2;"
            )
            highest_position = await hp_stmt.fetchrow(guild.id, self.parent_id)

            if highest_position is not None:
                highest_position: int = highest_position["position"]

                hp = highest_position or 0

            if self.position > hp + 1 or self.position < 0:
                raise CustomError("Invalid channel position")

            ep_stmt = await db.prepare(
                "UPDATE channels SET position = $2 WHERE position = $1"
            )
            await ep_stmt.executemany([self.__mover(db, ep_stmt, hp)])

    @classmethod
    async def create(
        cls,
        name: str,
        type: int,
        guild: Guild | None = None,
        parent: Channel | None = None,
        position: int | None = None,
    ) -> typing.Self:
        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "INSERT INTO channels (id, name, type, guild_id, parent_id, position) VALUES ($1, $2, $3, $4, $5, $6);"
            )

            channel_id = meta.genflake()

            if guild:
                hp_stmt = await db.prepare(
                    f"SELECT max(position) FROM channels WHERE guild_id = $1 AND parent_id = $2;"
                )
                highest_position = await hp_stmt.fetchrow(guild.id, parent.id)

                if highest_position is not None:
                    highest_position: int = highest_position["position"]

                if not position:
                    if highest_position is None:
                        cposition = 0
                    else:
                        cposition: int = highest_position["position"] + 1
                else:
                    hp = highest_position or 0

                    if position > hp + 1 or position < 0:
                        raise CustomError("Invalid channel position")

                    ep_stmt = await db.prepare(
                        "UPDATE channels SET position = $2 WHERE position = $1"
                    )

                    for i in range(hp):
                        if i >= position:
                            await ep_stmt.fetch(i, i + 1)
                        else:
                            await ep_stmt.fetch(i, i - 1)

                await stmt.fetch(channel_id, name, type, guild.id, parent.id, cposition)
            else:
                # TODO: actually handle to allow DM channels
                cposition = None

            return Channel(
                id=channel_id,
                name=name,
                type=type,
                guild_id=guild.id,
                last_message_id=None,
                parent=parent,
                position=cposition,
            )

    async def modify(self) -> None:
        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "UPDATE channels SET name = $2, last_message_id = $3, parent_id = $4, position = $5 WHERE id = $1"
            )
            await stmt.fetch(
                self.id, self.name, self.last_message_id, self.parent_id, self.position
            )

    async def delete(self) -> None:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("DELETE FROM channels WHERE id = $1;")
            await stmt.fetch(self.id)
