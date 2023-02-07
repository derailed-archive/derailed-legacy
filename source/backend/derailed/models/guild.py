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

from sqlalchemy import BigInteger, ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from logging import getLogger

from .base import Base

_log = getLogger(__name__)

class Guild(Base):
    __tablename__ = 'guilds'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    flags: Mapped[int]
    owner_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('users.id'))
    permissions: Mapped[int] = mapped_column(BigInteger())

    @classmethod
    async def get(cls, session: AsyncSession, guild_id: int) -> Guild | None:
        _log.debug(f'Getting guild {guild_id}')
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
        _log.debug(f'Getting invite {invite_id}')
        stmt = select(cls).where(Invite.id == invite_id)
        result = await session.execute(stmt)
        return result.scalar()
