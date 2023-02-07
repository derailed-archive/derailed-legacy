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

from enum import Enum
from logging import getLogger

from sqlalchemy import BigInteger, ForeignKey, String, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

__all__ = ['User', 'GuildPosition', 'Settings']


_log = getLogger()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    username: Mapped[str] = mapped_column(String(32), index=True)
    discriminator: Mapped[str] = mapped_column(String(4))
    email: Mapped[str] = mapped_column(index=True)
    password: Mapped[str]
    flags: Mapped[int]
    system: Mapped[bool]
    deletor_job_id: Mapped[int | None]
    suspended: Mapped[bool]

    @classmethod
    async def get(cls, session: AsyncSession, user_id: int) -> User | None:
        _log.debug(f'Getting user {user_id}')
        stmt = select(cls).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def get_email(cls, session: AsyncSession, email: str) -> User | None:
        _log.debug(f'Getting user from email {email}')
        stmt = select(cls).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalar()

    async def modify(self, session: AsyncSession, **modifications) -> None:
        stmt = update(User).where(User.id == self.id).values(**modifications)
        await session.execute(stmt)

        for name, value in modifications.items():
            setattr(name, value)

    @classmethod
    async def exists(
        cls, session: AsyncSession, username: str, discriminator: str
    ) -> bool:
        _log.debug(f'Checking if a user with username "{username}" and discriminator "{discriminator}" exists')
        stmt = (
            select(cls)
            .where(User.username == username)
            .where(User.discriminator == discriminator)
        )
        result = await session.execute(stmt)
        return result.scalar() is not None


class GuildPosition(Base):
    __tablename__ = 'guild_positions'

    user_id: Mapped[int] = mapped_column(
        BigInteger(), ForeignKey('users.id'), primary_key=True
    )
    guild_id: Mapped[int] = mapped_column(
        BigInteger(), ForeignKey('guilds.id'), primary_key=True
    )
    position: Mapped[int]

    @classmethod
    async def get_for(cls, session: AsyncSession, user: User) -> list[GuildPosition]:
        _log.debug(f'Getting all guild positions for {user.id}')
        stmt = (
            select(cls)
            .where(GuildPosition.user_id == user.id)
            .column(GuildPosition.guild_id)
            .column(GuildPosition.position)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def for_new(cls, session: AsyncSession, user_id: int) -> int:
        _log.debug(f'Getting higher position for user {user_id}')
        stmt = select(func.max(GuildPosition.position)).where(
            GuildPosition.user_id == user_id
        )
        result = await session.execute(stmt)
        scalar = result.scalar()

        if scalar is None:
            return 0
        else:
            return scalar.position + 1


class DefaultStatus(Enum):
    ONLINE = 'online'
    OFFLINE = 'invisible'
    BUSY = 'busy'
    BUST = 'dnd'


class Settings(Base):
    __tablename__ = 'settings'

    user_id: Mapped[int] = mapped_column(
        BigInteger(), ForeignKey('users.id'), primary_key=True
    )
    status: Mapped[DefaultStatus]

    @classmethod
    async def get(cls, session: AsyncSession, user: User) -> Settings | None:
        _log.debug(f'Getting settings for user {user.id}')
        stmt = select(cls).where(Settings.user_id == user.id)
        result = await session.execute(stmt)
        return result.scalar()
