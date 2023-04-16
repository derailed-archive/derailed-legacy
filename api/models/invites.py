# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from dataclasses import dataclass
from typing import Any

from .user import User

from .guild import Guild

from ..utils import MISSING, Maybe
from ..metadata import Object


@dataclass
class Invite(Object):
    id: str
    guild_id: int
    author_id: int
    channel_id: int
    created_at: str

    async def publicize(self, secure: bool = False, guild: Maybe[Guild] = MISSING, author: Maybe[User] = MISSING, channel: Maybe[Object] = MISSING) -> dict[str, Any]:
        if not guild:
            guild = await Guild.acquire(self.guild_id)

        if not author:
            author = await User.acquire(self.author_id)

        if not channel:
            channel = ...

        return {
            'id': self.id,
            'meta': {
                'guild': guild,
                'author': author,
                'channel': channel,  
            },
            'created_at': self.created_at
        }
