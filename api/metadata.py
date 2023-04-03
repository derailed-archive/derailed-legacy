# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

from __future__ import annotations

import os
import threading
import time
import typing

import asyncpg

if typing.TYPE_CHECKING:
    from .refs.current_user_ref import CurUserRef

__all__ = ("Meta", "Object", "meta")


class Meta:
    def __init__(self) -> None:
        self.cache: dict[str, Object] = {}
        self.token_cache: dict[str, CurUserRef] = {}
        self.curthread = threading.current_thread().ident
        self.pid = os.getpid()
        self._epoch = 1672531200000

    async def initialize(self) -> None:
        self.db = asyncpg.create_pool(os.environ["DATABASE_URL"])

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
    @classmethod
    def from_cache(self, object_id: int | str) -> typing.Self | None:
        return meta.cache.get(object_id)

    async def publicize(self, secure: bool = False) -> dict[str, typing.Any]:
        """Return a dictionary representation of this object for the general public.

        Parameters
        ----------
        secure: :class:`bool`
            Whether this is secure and can return sensitive data like emails.
        """
