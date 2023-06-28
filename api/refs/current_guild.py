# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from typing import Annotated

from fastapi import Depends, Path

from ..flags import RolePermissions
from ..models.guild import Guild
from ..models.member import Member
from ..models.user import User
from .base import Ref
from .current_user_ref import CurUserRef, cur_ref


class CurrentGuildRef(Ref):
    def __init__(self, guild_id: int, user: User) -> None:
        self.guild_id = guild_id
        self.user = user

    async def get_guild(self) -> Guild:
        return await Guild.acquire(self.guild_id)

    async def get_member(
        self,
        perm: int | RolePermissions | None = None,
        perms: list[int | RolePermissions] | None = None,
        guild: Guild | None = None,
    ) -> Member:
        member = await Member.acquire(self.user.id, self.guild_id)

        if guild:
            if perm is not None:
                await member.has_permissions([perm])
            elif perms:
                await member.has_permissions(perms)

        return member


async def cur_guild_ref(
    guild_id: Annotated[int, Path()], user_ref: Annotated[CurUserRef, Depends(cur_ref)]
) -> CurrentGuildRef:
    user = await user_ref.get_user()

    return CurrentGuildRef(guild_id=guild_id, user=user)
