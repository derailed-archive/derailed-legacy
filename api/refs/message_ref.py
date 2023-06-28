# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

from typing import Annotated

from fastapi import Depends, Path

from ..models.channel import Channel
from ..models.message import Message
from .base import Ref
from .channel_ref import ChannelRef, cur_channel_ref


class MessageRef(Ref):
    def __init__(self, message_id: int, channel: Channel) -> None:
        self.id = message_id
        self.channel = channel

    async def __activate(self) -> None:
        self.message = await Message.acquire(self.id, self.channel.id)


async def cur_message_ref(
    channel_ref: Annotated[ChannelRef, Depends(cur_channel_ref)],
    message_id: Annotated[str, Path()],
) -> MessageRef:
    ref = MessageRef(message_id, channel_ref.channel)
    await ref.__activate()
    return ref
