# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from dataclasses import dataclass
import typing

from ..api.errors import CustomError
from ..api.metadata import Object, meta


@dataclass
class Activity(Object):
    id: int
    user_id: int
    type: int
    content: str
    created_at: str

    async def publicize(self, secure: bool = False) -> dict[str, typing.Any]:
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'type': self.type,
            'content': self.content,
            'created_at': self.created_at
        }

    @classmethod
    async def acquire_all(cls, user_id: int) -> list[typing.Self]:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("SELECT * FROM activities WHERE user_id = $1;")

            rows = await stmt.fetch(user_id)

            for row in rows:
                return cls(
                    id=row['id'],
                    user_id=user_id,
                    type=row['type'],
                    content=row['content'],
                    created_at=row['created_at']
                )

    @classmethod
    async def acquire(cls, id: int) -> typing.Self:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("SELECT * FROM activities WHERE id = $1;")

            row = await stmt.fetchrow(id)

            if row is None:
                raise CustomError("Activity does not exist")

            return cls(
                id=id,
                user_id=row['user_id'],
                type=row['type'],
                content=row['content'],
                created_at=row['created_at']
            )

    @classmethod
    async def create(cls, user_id: int, type: int, content: str) -> None:
        ...
