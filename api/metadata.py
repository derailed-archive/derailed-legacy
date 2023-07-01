# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

from __future__ import annotations

import os
import threading
import time
import typing

import asyncpg
import grpc.aio as grpc

from .dgrpc import GuildStub, Interchange
from .dgrpc.gateway_pb2 import BulkInterchange, GuildInfo

__all__ = ("Meta", "Object", "meta")


class GuildMetadata(typing.TypedDict):
    presences: int
    available: bool


class Meta:
    def __init__(self) -> None:
        self.curthread = threading.current_thread().ident
        self.pid = os.getpid()
        self._epoch = 1672531200000
        self._incr = 0
        self._grpc_stub = None

    async def initialize(self) -> None:
        self.db = await asyncpg.create_pool(os.environ["DATABASE_URL"])
        if os.getenv("GRPC_URL") is not None:
            channel = grpc.insecure_channel(os.environ["GRPC_URL"])
            self._grpc_stub = GuildStub(channel)

    async def dispatch_guild(self, type: str, guild_id: int, data: typing.Any) -> None:
        if self._grpc_stub:
            await self._grpc_stub.dispatch_guild(
                Interchange(t=type, id=guild_id, d=data)
            )

    async def dispatch_user(self, type: str, user_id: int, data: typing.Any) -> None:
        if self._grpc_stub:
            await self._grpc_stub.dispatch_user(Interchange(t=type, id=user_id, d=data))

    async def dispatch_bulk(
        self, type: str, data: typing.Any, users: list[int]
    ) -> None:
        if self._grpc_stub:
            await self._grpc_stub.dispatch_user(
                BulkInterchange(t=type, uids=users, d=data)
            )

    async def get_guild_metadata(self, guild_id: int) -> GuildMetadata:
        if self._grpc_stub:
            metadata = await self._grpc_stub.get_metadata(GuildInfo(id=guild_id))
            return {"presences": metadata.presences, "available": metadata.available}
        else:
            return {"presences": 0, "available": False}

    def genflake(self) -> int:
        current_ms = int(time.time() * 1000)
        epoch = current_ms - self._epoch << 22

        if self.curthread is None:
            raise AssertionError

        epoch |= (self.curthread % 32) << 17
        epoch |= (self.pid % 32) << 12

        epoch |= self._incr % 4096

        if self._incr == 9000000000:
            self._incr = 0

        self._incr += 1

        return epoch


meta = Meta()


class Object:
    async def publicize(self, secure: bool = False) -> dict[str, typing.Any]:
        """Return a dictionary representation of this object for the general public.

        Parameters
        ----------
        secure: :class:`bool`
            Whether this is secure and can return sensitive data like emails.
        """

    async def partialize(self, *args: str) -> dict[str, typing.Any]:
        """Return a partial dictionary representation of this object for the general public."""

        pub = await self.publicize()

        return {arg: pub[arg] for arg in args}
