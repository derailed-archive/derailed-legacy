"""
Copyright (C) 2021-2023 Derailed.

Under no circumstances may you publicly share, distribute, or give any objects, files, or media in this project.
You may only share the above with individuals who have permission to view these files already.
If they don't have permission but are still given the files, or if code is shared publicly, 
we have the legal jurisdiction to bring forth charges under which is owed, based in the damages.

You may under some circumstances with authorized permission share snippets of the code for specific reasons.
Any media and product here must be kept proprietary unless otherwise necessary or authorized.
"""
from __future__ import annotations

from enum import Enum

from sqlalchemy import BigInteger, ForeignKey, String, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

__all__ = ['User', 'GuildPosition', 'Settings']


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
        stmt = select(cls).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def get_email(cls, session: AsyncSession, email: str) -> User | None:
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
        stmt = select(cls).where(Settings.user_id == user.id)
        result = await session.execute(stmt)
        return result.scalar()
