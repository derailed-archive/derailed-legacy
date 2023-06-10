# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from typing import Annotated

from fastapi import APIRouter

from api.refs import channel_ref

from ..models.channel import Channel
from ..models.read_states import ReadState
from ..refs.channel_ref import ChannelRef
from ..refs.current_guild import CurrentGuildRef, cur_guild_ref
from ..refs.current_user_ref import CurUserRef, cur_ref

router = APIRouter()


@router.get("/read_states")
async def get_read_states(user_ref: Annotated[CurUserRef, cur_ref]):
    user = await user_ref.get_user()

    read_states = await ReadState.acquire_all(user.id)

    return [await read_state.publicize() for read_state in read_states]


@router.get("/guilds/{guild_id}/read_states")
async def get_guild_read_states(guild_ref: Annotated[CurrentGuildRef, cur_guild_ref]):
    guild = await guild_ref.get_guild()
    member = await guild_ref.get_member(guild=guild)

    channels = await Channel.acquire_all(guild.id)

    read_states = await ReadState.acquire_mass(
        member.id, [channel.id for channel in channels]
    )

    return [await read_state.publicize() for read_state in read_states]


@router.delete("/guilds/{guild_id}/read_states")
async def delete_guild_read_states(
    guild_ref: Annotated[CurrentGuildRef, cur_guild_ref]
):
    guild = await guild_ref.get_guild()
    member = await guild_ref.get_member(guild=guild)

    channels = await Channel.acquire_all(guild.id)
    channel_map = {channel.id: channel for channel in channels}

    read_states = await ReadState.acquire_mass(
        member.id, [channel.id for channel in channels]
    )

    updated = {}

    for read_state in read_states:
        channel = channel_map[read_state.channel_id]
        updated[read_state] = channel.last_message_id

    await ReadState.mass_modify(updated)

    return ""


@router.delete("/channel/{channel_id}/ack")
async def acknowledge_channel(channel_ref: Annotated[ChannelRef, channel_ref]):
    read_state = await ReadState.acquire(channel_ref.user.id, channel_ref.channel_id)

    read_state.last_message_id = channel_ref.channel.last_message_id

    await read_state.modify()

    return ""
