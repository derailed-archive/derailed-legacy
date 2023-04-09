# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


import typing
from dataclasses import dataclass
from datetime import datetime

from ..metadata import Object


@dataclass
class Member(Object):
    """Represents a Derailed Guild member."""

    user_id: int
    guild_id: int
    nick: str | None
    joined_at: datetime

    @classmethod
    async def acquire(self) -> typing.Self:
        ...
