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

from sqlalchemy import BigInteger, ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Guild(Base):
    __tablename__ = 'guilds'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    flags: Mapped[int]
    owner_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('users.id'))
    permissions: Mapped[int] = mapped_column(BigInteger())

    @classmethod
    async def get(cls, session: AsyncSession, guild_id: int) -> Guild | None:
        stmt = select(cls).where(Guild.id == guild_id)
        result = await session.execute(stmt)
        return result.scalar()


class Invite(Base):
    __tablename__ = 'invites'

    id: Mapped[str] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('guilds.id'))
    author_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('users.id'))
    channel_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('channels.id'))

    @classmethod
    async def get(cls, session: AsyncSession, invite_id: str) -> Invite | None:
        stmt = select(cls).where(Invite.id == invite_id)
        result = await session.execute(stmt)
        return result.scalar()
