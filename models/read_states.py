# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


import typing
from dataclasses import dataclass

from ..api.errors import CustomError
from ..api.metadata import Object, meta


@dataclass
class ReadState(Object):
    channel_id: int
    user_id: int
    last_message_id: int

    async def publicize(self, secure: bool = False) -> dict[str, typing.Any]:
        return {
            'channel_id': str(self.channel_id),
            'last_message_id': str(self.last_message_id)
        }

    @property
    def info(self):
        return self.channel_id, self.user_id

    @classmethod
    async def acquire(cls, user_id: int, channel_id: int) -> typing.Self:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("SELECT * WHERE channel_id = $1 AND user_id = $2;")
            row = await stmt.fetchrow(user_id, channel_id)

            if row is None:
                raise CustomError("Read state does not exist", 404)

        return ReadState(channel_id, user_id, row.get("last_message_id"))

    @classmethod
    async def acquire_mass(
        cls, user_id: int, channel_ids: list[int]
    ) -> list[typing.Self]:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("SELECT * WHERE channel_id = $1 AND user_id = $2;")
            rows = await stmt.executemany(
                [(user_id, channel_id) for channel_id in channel_ids]
            )

        read_states = []

        for row in rows:
            if row is not None:
                read_states.append(
                    ReadState(row["channel_id"], user_id, row.get("last_message_id"))
                )

        return read_states

    @classmethod
    async def acquire_all(cls, user_id: int) -> list[typing.Self]:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("SELECT * WHERE user_id = $1;")
            rows = await stmt.fetch(user_id)

        read_states = []

        for row in rows:
            read_states.append(
                ReadState(row["channel_id"], user_id, row.get("last_message_id"))
            )

        return read_states

    @classmethod
    async def create(
        cls, channel_id: int, user_id: int, last_message_id: int
    ) -> typing.Self:
        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "INSERT INTO read_states (channel_id, user_id, last_message_id) VALUES ($1, $2, $3);"
            )
            await stmt.fetch(channel_id, user_id, last_message_id)

        return ReadState(channel_id, user_id, last_message_id)

    async def modify(self) -> None:
        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "UPDATE read_states SET last_message_id = $3 WHERE channel_id = $1 AND user_id = $2;"
            )
            await stmt.fetch(self.last_message_id)

    async def delete(self) -> None:
        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "DELETE FROM read_states WHERE channel_id = $1 AND user_id = $2;"
            )
            await stmt.fetch(self.channel_id, self.user_id)

    @classmethod
    async def mass_delete(self, read_states: list[typing.Self]) -> None:
        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "DELETE FROM read_states WHERE channel_id = $1 AND user_id = $2 AND EXISTS (SELECT 1 FROM read_states WHERE channel_id = $1 AND user_id = $2);"
            )
            await stmt.executemany(
                [
                    (read_state.channel_id, read_state.user_id)
                    for read_state in read_states
                ]
            )

    @classmethod
    async def mass_modify(self, read_state_updates: dict[typing.Self, int]) -> None:
        updates = []

        for key, value in read_state_updates.items():
            updates.append((key.channel_id, key.user_id, value))

        if updates == []:
            return

        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "UPDATE read_states SET last_message_id = $3 WHERE channel_id = $1 AND user_id = $2;"
            )
            await stmt.executemany(updates)
