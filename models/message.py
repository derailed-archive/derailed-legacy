# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


import typing
from dataclasses import dataclass
from datetime import datetime

from ..api.errors import CustomError
from ..api.metadata import Object, meta
from ..api.utils import date_or_none


@dataclass
class Message(Object):
    id: int
    channel_id: int
    author_id: int
    content: str
    timestamp: datetime
    edited_timestamp: datetime | None

    async def publicize(self, secure: bool = False) -> dict[str, typing.Any]:
        return {
            "id": str(self.id),
            "channel_id": str(self.channel_id),
            "author_id": str(self.author_id),
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "edited_timestamp": self.edited_timestamp.isoformat(),
        }

    @classmethod
    async def acquire(cls, message_id: int, channel_id: int) -> typing.Self:
        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "SELECT * FROM messages WHERE id = $1 AND channel_id = $2;"
            )

            message = await stmt.fetchrow(message_id, channel_id)

            if message is None:
                raise CustomError("Message does not exist", code=404)

        return cls(
            id=message_id,
            channel_id=channel_id,
            author_id=message["author_id"],
            content=message["content"],
            timestamp=datetime.fromisoformat(message["timestamp"]),
            edited_timestamp=date_or_none(message.get("edited_timestamp")),
        )

    @classmethod
    async def acquire_all(cls, channel_id: int) -> list[typing.Self]:
        msgs = []

        async with meta.db.acquire() as db:
            stmt = await db.prepare("SELECT * FROM messages WHERE channel_id = $1;")
            vals = await stmt.fetch(channel_id)

        for msg in vals:
            msgs.append(
                cls(
                    id=msg["id"],
                    channel_id=channel_id,
                    author_id=msg["author_id"],
                    content=msg["content"],
                    timestamp=datetime.fromisoformat(msg["timestamp"]),
                    edited_timestamp=date_or_none(msg.get("edited_timestamp")),
                )
            )

        return msgs

    @classmethod
    async def create(cls, author_id: int, content: str, channel_id: int) -> typing.Self:
        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "INSERT INTO messages (id, channel_id, author_id, content, timestamp) VALUES ($1, $2, $3, $4, $5);"
            )

            message_id = meta.genflake()
            timestamp = datetime.utcnow()

            await stmt.fetch(
                message_id, channel_id, author_id, content, timestamp.isoformat()
            )

        return cls(
            id=message_id,
            channel_id=channel_id,
            author_id=author_id,
            content=content,
            timestamp=timestamp,
            edited_timestamp=None,
        )

    async def modify(self) -> None:
        async with meta.db.acquire() as db:
            stmt = await db.prepare(
                "UPDATE messages SET content = $2, edited_timestamp = $3 WHERE id = $1"
            )
            await stmt.fetch(self.id, self.content, self.edited_timestamp)

    async def delete(self) -> None:
        async with meta.db.acquire() as db:
            stmt = await db.prepare("DELETE FROM messages WHERE id = $1;")
            await stmt.fetch(self.id)
