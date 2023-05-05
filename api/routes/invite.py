# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel

from ..errors import CustomError
from ..flags import RolePermissions
from ..metadata import meta
from ..models.member import Member
from ..refs.current_guild import CurrentGuildRef, cur_guild_ref
from ..refs.current_user_ref import CurUserRef, cur_ref
from ..refs.invite_ref import InviteRef, invite_ref

route_invites = APIRouter()


@route_invites.get("/invites/{invite_id}")
async def get_invite(invite_ref: Annotated[InviteRef, invite_ref]):
    invite = await invite_ref.get()

    return invite.publicize()


@route_invites.post("/invites/{invite_id}/join")
async def join_guild(
    invite_ref: Annotated[InviteRef, invite_ref],
    cur_user: Annotated[CurUserRef, cur_ref],
):
    user = await cur_user.get_user()

    invite = await invite_ref.get()
    try:
        Member.acquire(user.id, invite.guild_id)
    except CustomError:
        pass
    else:
        raise CustomError("Already a member of this Guild")

    member = await Member.join(user.id, invite.guild_id)

    await meta.dispatch_guild("MEMBER_JOIN", member.guild_id, await member.publicize())

    return await member.publicize()


# TODO: requires channels.
@route_invites.post("/guilds/{guild_id}/channels/{}/invites")
async def create_invite(guild_ref: Annotated[CurrentGuildRef, cur_guild_ref]):
    ...


@route_invites.delete("/guilds/{guild_id}/invites/{invite_id}")
async def delete_guild_invite(
    invite_ref: Annotated[InviteRef, invite_ref],
    cur_guild: Annotated[CurrentGuildRef, cur_guild_ref],
):
    await cur_guild.get_member(RolePermissions.MANAGE_INVITES)

    invite = await invite_ref.get()

    await invite.delete()

    return ""
