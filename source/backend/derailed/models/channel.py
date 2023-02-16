"""
Copyright (C) 2021-2023 Derailed

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import BigInteger, ForeignKey, String, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from logging import getLogger

from .base import Base


_log = getLogger()


class ReadState(Base):
    __tablename__ = 'readstates'

    user_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('users.id'), primary_key=True)
    channel_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('channels.id'), primary_key=True)
    mentions: Mapped[int]
    last_read_message: Mapped[int] = mapped_column(BigInteger(), ForeignKey('messages.id'))

    @classmethod
    async def get_all(cls, session: AsyncSession, user_id: int) -> list[ReadState]:
        _log.debug(f'Getting readstates for {user_id}')
        stmt = (
            select(cls)
            .where(ReadState.user_id == user_id)
        )
        result = await session.execute(stmt)
        return result.scalars().all()


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    author_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('users.id'))
    content: Mapped[str] = mapped_column(String(2024))
    channel_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('channels.id'))
    timestamp: Mapped[datetime]
    edited_timestamp: Mapped[datetime | None]

    @classmethod
    async def sorted_channel(
        cls, session: AsyncSession, channel: Channel, limit: int
    ) -> list[Message]:
        _log.debug(f'Sorting all messages in channel {channel.id} with limit {limit}')
        stmt = (
            select(cls)
            .where(Message.channel_id == channel.id)
            .order_by(Message.id.desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get(
        cls, session: AsyncSession, message_id: int, channel: Channel
    ) -> Message | None:
        _log.debug(f'Attempting to get message {message_id} from channel {channel.id}')
        stmt = (
            select(cls)
            .where(Message.id == message_id)
            .where(Message.channel_id == channel.id)
        )
        result = await session.execute(stmt)
        return result.scalar()

    async def delete(self, session: AsyncSession, message_id: int) -> None:
        _log.debug(f'Deleting message {message_id}')
        stmt = delete(Message).where(Message.id == message_id)
        await session.execute(stmt)


class ChannelType(Enum):
    CATEGORY = 0
    TEXT = 1


class ChannelMember(Base):
    __tablename__ = 'channel_members'

    channel_id: Mapped[int] = mapped_column(
        BigInteger(), ForeignKey('channels.id'), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('users.id'))


class Channel(Base):
    __tablename__ = 'channels'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    type: Mapped[ChannelType]
    name: Mapped[str | None] = mapped_column(String(32))
    last_message_id: Mapped[int | None] = mapped_column(ForeignKey('messages.id'))
    parent_id: Mapped[int | None] = mapped_column(ForeignKey('channels.id'))
    guild_id: Mapped[int | None] = mapped_column(ForeignKey('guilds.id'))
    position: Mapped[int | None]
    message_deletor_job_id: Mapped[str | None]

    @classmethod
    async def get(
        cls, session: AsyncSession, id: int, guild_id: int | None = None
    ) -> 'Channel' | None:
        _log.debug(f'Getting channel {id} from guild {guild_id}')
        stmt = select(cls).where(Channel.id == int(id))

        if guild_id:
            stmt = stmt.where(Channel.guild_id == guild_id)

        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def get_all(cls, session: AsyncSession, guild_id: int) -> list['Channel']:
        _log.debug(f'Getting all channels from guild {guild_id}')
        stmt = select(cls).where(Channel.guild_id == guild_id)

        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_with_pos(
        cls, session: AsyncSession, id: int, position: int, guild_id: int
    ) -> 'Channel' | None:
        _log.debug(f'Getting channel id {id} with position {position} from guild {guild_id}')
        stmt = (
            select(cls)
            .where(Channel.id == id)
            .where(Channel.position == position)
            .where(Channel.guild_id == guild_id)
        )
        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def get_for_pos(
        cls,
        session: AsyncSession,
        position: int,
        guild_id: int,
        category: int | None = None,
    ) -> 'Channel' | None:
        _log.debug(f'Getting channel with position {position} in guild {guild_id} and category {category}')
        stmt = (
            select(cls)
            .where(Channel.position == position)
            .where(Channel.guild_id == guild_id)
            .where(Channel.parent_id == category)
        )
        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def get_via_with(
        cls, session: AsyncSession, id: int, category_id: int, guild_id: int
    ) -> 'Channel' | None:
        _log.debug(f'Getting channel {id} in category {category_id} from guild {guild_id}')
        stmt = (
            select(cls)
            .where(Channel.id == id)
            .where(Channel.parent_id == category_id)
            .where(Channel.guild_id == guild_id)
        )

        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def get_via(
        cls, session: AsyncSession, category_id: int | None, guild_id: int
    ) -> list['Channel']:
        _log.debug(f'Getting all channels in {category_id} from {guild_id}')
        stmt = (
            select(cls)
            .where(Channel.parent_id == category_id)
            .where(Channel.guild_id == guild_id)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def count(cls, session: AsyncSession, guild_id: int) -> int:
        _log.debug(f'Counting all channels from guild {guild_id}')
        stmt = select(func.count(Channel.guild_id)).where(Channel.guild_id == guild_id)
        return (await session.execute(stmt)).scalar()

    @classmethod
    async def highest(
        cls, session: AsyncSession, guild_id: int, category: int | None = None
    ) -> Channel | None:
        _log.debug(f'Getting highest channel in {guild_id} with category {category}')
        stmt = (
            select(func.max(Channel.position))
            .where(Channel.guild_id == guild_id)
            .where(Channel.parent_id == category)
        )
        result = await session.execute(stmt)
        return result.scalar()

    async def modify(self, session: AsyncSession, **modifications) -> None:
        stmt = update(Channel).where(Channel.id == self.id).values(**modifications)
        await session.execute(stmt)

        for name, value in modifications.items():
            setattr(name, value)

    async def delete(self, session: AsyncSession) -> None:
        _log.debug(f'Deleting channel {self.id} in category {self.parent_id} from guild {self.guild_id}')
        stmt = delete(Channel).where(Channel.id == self.id)
        await session.execute(stmt)
