# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

from typing import Annotated, Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from api.metadata import meta
from api.refs import channel_ref

from ..errors import CustomError
from ..flags import RolePermissions
from ..models.channel import Channel
from ..refs.current_guild import CurrentGuildRef, cur_guild_ref
from ..utils import MISSING, Maybe, channel_or_none

router = APIRouter()


class CreateChannel(BaseModel):
    name: str = Field(max_length=32, min_length=1)
    type: Literal[0, 1]
    parent_id: int | None = Field(None)
    position: int | None = Field(None)


class ModifyChannel(BaseModel):
    name: str | None = Field(None, max_length=32, min_length=1)
    parent_id: Maybe[int | None] = Field(MISSING)
    position: int | None = Field(None)


@router.get("/guilds/{guild_id}/channels")
async def get_guild_channels(guild_ref: Annotated[CurrentGuildRef, cur_guild_ref]):
    await guild_ref.get_member(perm=RolePermissions.VIEW_CHANNELS)

    channels = await Channel.acquire_all(guild_ref.guild_id)

    return [await channel.publicize() for channel in channels]


@router.get("/guilds/{guild_id}/channels/{channel_id}")
async def get_guild_channels(
    guild_ref: Annotated[CurrentGuildRef, cur_guild_ref],
    channel_ref: Annotated[channel_ref.ChannelRef, channel_ref.cur_channel_ref],
):
    await guild_ref.get_member(perm=RolePermissions.VIEW_CHANNELS)

    return await channel_ref.channel.publicize()


@router.post("/guilds/{guild_id}/channels")
async def create_channel(
    guild_ref: Annotated[CurrentGuildRef, cur_guild_ref], payload: CreateChannel
):
    await guild_ref.get_member(perm=RolePermissions.MANAGE_CHANNELS)

    channel = await Channel.create(
        name=payload.name,
        type=payload.type,
        guild=await guild_ref.get_guild(),
        parent=await channel_or_none(payload.parent_id),
        position=payload.position,
    )

    pub = await channel.publicize()

    await meta.dispatch_guild("CHANNEL_CREATE", guild_ref.guild_id, pub)

    return pub


@router.patch("/guilds/{guild_id}/channels/{channel_id}")
async def modify_channel(
    guild_ref: Annotated[CurrentGuildRef, cur_guild_ref],
    channel_ref: Annotated[channel_ref.ChannelRef, channel_ref.cur_channel_ref],
    payload: ModifyChannel,
):
    guild = await guild_ref.get_guild()
    await guild_ref.get_member(perm=RolePermissions.MANAGE_CHANNELS, guild=guild)
    channel = channel_ref.channel

    if payload.name:
        channel.name = payload.name

    if payload.parent_id is not MISSING:
        parent_channel = None
        if payload.parent_id is not None:
            parent_channel = await Channel.acquire(payload.parent_id)
            if parent_channel.guild_id != guild_ref.guild_id:
                raise CustomError("parent_id must match a channel inside of guild")

        channel.parent = parent_channel

    if payload.position is not None and payload.position != channel.position:
        channel.position = payload.position
        await channel.move(guild)

    pub = await channel.publicize()

    await meta.dispatch_guild("CHANNEL_EDIT", guild.id, pub)

    return pub


@router.delete("/guilds/{guild_id}/channels/{channel_id}")
async def delete_channel(
    guild_ref: Annotated[CurrentGuildRef, cur_guild_ref],
    channel_ref: Annotated[channel_ref.ChannelRef, channel_ref.cur_channel_ref],
):
    guild = await guild_ref.get_guild()
    await guild_ref.get_member(perm=RolePermissions.MANAGE_CHANNELS, guild=guild)
    channel = channel_ref.channel

    await channel.delete()

    await meta.dispatch_guild(
        "CHANNEL_DELETE",
        guild.id,
        {"channel_id": channel.id, "guild_id": channel.guild_id},
    )

    return ""
