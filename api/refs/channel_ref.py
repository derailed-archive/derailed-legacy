# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from typing import Annotated

from fastapi import Path

from ..models.channel import Channel
from ..models.user import User
from .base import Ref
from .current_user_ref import CurUserRef, cur_ref


class ChannelRef(Ref):
    channel_id: int
    channel: Channel

    def __init__(self, channel_id: int, user: User) -> None:
        self.channel_id = channel_id
        self.user = user

    async def _organize(self) -> None:
        self.channel = await Channel.acquire(self.channel_id)

        # TODO: check guild perms & overwrite perms


async def cur_channel_ref(
    channel_id: Annotated[str, Path()], user_ref: Annotated[CurUserRef, cur_ref]
) -> ChannelRef:
    ref = ChannelRef(channel_id, await user_ref.get_user())
    await ref._organize()

    return ref
