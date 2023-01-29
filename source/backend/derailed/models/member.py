"""
Copyright (C) 2021-2023 Derailed.

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
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .guild import Guild
from .user import User


class RolePermissions(Base):
    __tablename__ = 'role_permissions'

    role_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('roles.id'), primary_key=True)
    allow: Mapped[int] = mapped_column(BigInteger())
    deny: Mapped[int] = mapped_column(BigInteger())


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    guild_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('guilds.id'), index=True)
    name: Mapped[str]
    permissions: Mapped[RolePermissions] = relationship()
    position: Mapped[int]

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Role | None:
        stmt = select(cls).where(Role.id == id)
        result = await session.execute(stmt)
        return result.scalar()


class MemberRole(Base):
    __tablename__ = 'member_roles'

    user_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('users.id'), primary_key=True)
    role_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('roles.id'), primary_key=True)
    guild_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('guilds.id'))


class Member(Base):
    __tablename__ = 'members'

    user_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('users.id'), primary_key=True)
    guild_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('guilds.id'), primary_key=True)
    nick: Mapped[str | None] = mapped_column(String(32))

    @classmethod
    async def get(cls, session: AsyncSession, user_id: int, guild_id: int) -> Member | None:
        stmt = select(cls).where(Member.user_id == user_id).where(Member.guild_id == guild_id)
        result = await session.execute(stmt)
        return result.scalar()
