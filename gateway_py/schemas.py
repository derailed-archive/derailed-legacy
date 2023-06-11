# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

from typing import Any, Literal
from pydantic import BaseModel


class BasicMessage(BaseModel):
    j: Literal[1]
    d: dict[str, Any]


class Identify(BaseModel):
    token: str
