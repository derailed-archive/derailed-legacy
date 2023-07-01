# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

from __future__ import annotations

import asyncio
import base64
import binascii
from typing import TYPE_CHECKING, Any

import itsdangerous

from api.metadata import meta

from ..api.errors import UserDoesNotExist
from ..api.utils import *
from .models import User

if TYPE_CHECKING:
    from .session import Session


async def broadcast(message: Any, clients: list) -> None:
    await asyncio.gather(**[client.send_text(message) for client in clients])


subscriptions: dict[int, list[Session]] = {}
presences: dict[int, dict[str, Any]]


async def publish(sub_id: int, data: dict, type: str) -> None:
    await asyncio.gather(*[ws.send(0, data, type) for ws in subscriptions[sub_id]])


async def bulk_publish(sub_ids: list[int], data: dict, type: str) -> None:
    funcs = [meta.d(type, sub_id, data) for sub_id in sub_ids]
    await asyncio.gather(*funcs)


def get_token_user_id(token: str) -> str:
    fragmented = token.split(".")
    encoded_id = fragmented[0]

    return int(base64.b64decode(encoded_id.encode()).decode())


def verify_token(user: User, token: str) -> None:
    signer = itsdangerous.TimestampSigner(user.password)

    try:
        signer.unsign(token)
    except itsdangerous.BadSignature:
        raise ValueError


async def tokenizer(token: str) -> User:
    try:
        user_id = get_token_user_id(token)
    # try to prevent every error and spin it back to the user
    except (IndexError, binascii.Error, UnicodeDecodeError):
        raise ValueError

    try:
        user = await User.acquire(user_id)
    except UserDoesNotExist:
        raise ValueError

    verify_token(user, token)

    return user
