# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..errors import CustomError
from ..flags import RolePermissions
from ..models.guild import Guild
from ..refs.current_guild import CurrentGuildRef, cur_guild_ref
from ..refs.current_user_ref import CurUserRef, cur_ref

route_guilds = APIRouter()


class CreateGuild(BaseModel):
    name: str = Field(min_length=1, max_length=32)


@route_guilds.post("/guilds")
async def create_guild(cur_user: Annotated[CurUserRef, cur_ref], payload: CreateGuild):
    user = await cur_user.get_user()

    guild = await Guild.create(payload.name, user.id)

    return await guild.publicize()


@route_guilds.get("/guilds/{guild_id}")
async def get_guild(cur_guild: Annotated[CurrentGuildRef, cur_guild_ref]):
    await cur_guild.get_member()

    return await (await cur_guild.get_guild()).publicize()


# TODO: add gateway calls
@route_guilds.get("/guilds/{guild_id}/preview")
async def get_guild(cur_guild: Annotated[CurrentGuildRef, cur_guild_ref]):
    return await (await cur_guild.get_guild()).publicize()


@route_guilds.patch("/guilds/{guild_id}")
async def modify_guild(
    cur_guild: Annotated[CurrentGuildRef, cur_guild_ref], payload: CreateGuild
):
    guild = await cur_guild.get_guild()
    await cur_guild.get_member(RolePermissions.MANAGE_GUILD, guild=guild)

    guild.name = payload.name

    await guild.modify()

    return await guild.publicize()


@route_guilds.delete("/guilds/{guild_id}")
async def delete_guild(cur_guild: Annotated[CurrentGuildRef, cur_guild_ref]):
    guild = await cur_guild.get_guild()

    if guild.owner_id != cur_guild.user.id:
        raise CustomError("Must be owner to delete guild")

    await guild.delete()

    return ""
