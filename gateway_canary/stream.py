# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

import asyncio

import msgspec

from .utils import publish
from ..api.metadata import meta


class Stream:
    def __init__(self) -> None:
        self._pubsub = None
        self._ready = False

    async def _recv(self) -> None:
        async for msg in self._pubsub.listen():
            data = msgspec.msgpack.decode(msg)
            await publish(data['id'], data["d"], data["t"])

    async def start(self) -> None:
        if not self._ready:
            self._ready = True
            await meta.initialize()

            self._pubsub = meta._redis.pubsub()
            self._pubsub.subscribe('main')

            asyncio.create_task(self._recv())

stream = Stream()
