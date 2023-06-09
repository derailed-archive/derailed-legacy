# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..metadata import meta
from ..models.message import Message
from ..refs.channel_ref import ChannelRef, cur_channel_ref
from ..refs.message_ref import MessageRef, cur_message_ref

router = APIRouter()


class CreateMessage(BaseModel):
    content: str = Field(min_length=1, max_length=8192)


@router.get("/channels/{channel_id}/messages")
async def get_channel_messages(channel_ref: Annotated[ChannelRef, cur_channel_ref]):
    msgs = await Message.acquire_all(channel_id=channel_ref.channel_id)

    return [await msg.publicize() for msg in msgs]


@router.get("/channels/{channel_id}/messages/{message_id}")
async def get_channel_message(message_ref: Annotated[MessageRef, cur_message_ref]):
    return await message_ref.message.publicize()


@router.post("/channels/{channel_id}/messages")
async def create_message(
    channel_ref: Annotated[ChannelRef, cur_channel_ref], payload: CreateMessage
):
    
    message = await Message.create(
        channel_ref.user.id, payload.content, channel_ref.channel_id
    )

    pub = await message.publicize()

    await meta.dispatch_guild("MESSAGE_CREATE", channel_ref.channel.guild_id, pub)

    return pub


@router.patch("/channels/{channel_id}/messages/{message_id}")
async def modify_message(
    message_ref: Annotated[MessageRef, cur_message_ref], payload: CreateMessage
):
    message = message_ref.message

    message.content = payload.content

    await message.modify()

    pub = await message.publicize()

    await meta.dispatch_guild("MESSAGE_EDIT", message_ref.channel.guild_id, pub)

    return pub


@router.delete("/channels/{channel_id}/messages/{message_id}")
async def delete_message(message_ref: Annotated[MessageRef, cur_message_ref]):
    await message_ref.message.delete()

    await meta.dispatch_guild(
        "MESSAGE_DELETE",
        message_ref.channel.guild_id,
        {
            "message_id": message_ref.id,
            "channel_id": message_ref.channel.id,
            "guild_id": message_ref.channel.guild_id,
        },
    )

    return ""
