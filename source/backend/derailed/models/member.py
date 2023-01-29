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
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class RolePermissions(Base):
    __tablename__ = 'role_permissions'

    role_id: Mapped[int] = mapped_column(
        BigInteger(), ForeignKey('roles.id'), primary_key=True
    )
    allow: Mapped[int] = mapped_column(BigInteger())
    deny: Mapped[int] = mapped_column(BigInteger())


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    guild_id: Mapped[int] = mapped_column(
        BigInteger(), ForeignKey('guilds.id'), index=True
    )
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

    user_id: Mapped[int] = mapped_column(
        BigInteger(), ForeignKey('users.id'), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        BigInteger(), ForeignKey('roles.id'), primary_key=True
    )
    guild_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('guilds.id'))


class Member(Base):
    __tablename__ = 'members'

    user_id: Mapped[int] = mapped_column(
        BigInteger(), ForeignKey('users.id'), primary_key=True
    )
    guild_id: Mapped[int] = mapped_column(
        BigInteger(), ForeignKey('guilds.id'), primary_key=True
    )
    nick: Mapped[str | None] = mapped_column(String(32))

    @classmethod
    async def get(
        cls, session: AsyncSession, user_id: int, guild_id: int
    ) -> Member | None:
        stmt = (
            select(cls)
            .where(Member.user_id == user_id)
            .where(Member.guild_id == guild_id)
        )
        result = await session.execute(stmt)
        return result.scalar()
