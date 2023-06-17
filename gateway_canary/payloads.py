# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

from typing import Literal

from pydantic import BaseModel, Field


class Base(BaseModel):
    op: Literal[1, 3, 4, 8]
    d: dict


class Identify(BaseModel):
    token: str
    client_status: str


class ActivityUpdate(BaseModel):
    type: Literal[0]
    content: str = Field(min_length=1, max_length=32)


class UpdatePresence(BaseModel):
    status: Literal[0, 1, 2, 3]
    activities: list[ActivityUpdate]


class GetMembers(BaseModel):
    guild_id: int


class HeartbeatResponse(BaseModel):
    id: str
