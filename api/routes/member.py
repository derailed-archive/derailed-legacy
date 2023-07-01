# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from typing import Annotated

from fastapi import APIRouter, Depends, Path
from pydantic import BaseModel, Field

from ..flags import RolePermissions
from ..metadata import meta
from ..models.member import Member
from ..refs.current_guild import CurrentGuildRef, cur_guild_ref
from ..utils import MISSING, Maybe

route_members = APIRouter()


class ModifyMember(BaseModel):
    nick: Maybe[str | None] = Field(MISSING, min_length=1, max_length=32)


@route_members.patch("/guilds/{guild_id}/members/@me")
async def modify_own_member(
    cur_guild: Annotated[CurrentGuildRef, Depends(cur_guild_ref)], payload: ModifyMember
):
    member = await cur_guild.get_member()

    member.nick = payload.nick

    await member.modify()

    await meta.dispatch_guild(
        "MEMBER_EDIT", cur_guild.guild_id, await member.publicize()
    )

    return await member.publicize()


@route_members.patch("/guilds/{guild_id}/members/{user_id}/nick")
async def modify_member_nick(
    cur_guild: Annotated[CurrentGuildRef, Depends(cur_guild_ref)],
    user_id: Annotated[int, Path()],
    payload: ModifyMember,
):
    await cur_guild.get_member(RolePermissions.MANAGE_NICKNAMES)

    member = await Member.acquire(user_id, cur_guild.guild_id)

    member.nick = payload.nick

    await member.modify()

    await meta.dispatch_guild(
        "MEMBER_EDIT", cur_guild.guild_id, await member.publicize()
    )

    return await member.publicize()


@route_members.patch("/guilds/{guild_id}/members/{user_id}")
async def modify_member(
    cur_guild: Annotated[CurrentGuildRef, Depends(cur_guild_ref)],
    user_id: Annotated[int, Path()],
    payload: ModifyMember,
):
    await cur_guild.get_member(RolePermissions.MANAGE_MEMBERS)

    member = await Member.acquire(user_id, cur_guild.guild_id)

    member.nick = payload.nick

    await member.modify()

    await meta.dispatch_guild(
        "MEMBER_EDIT", cur_guild.guild_id, await member.publicize()
    )

    return await member.publicize()
