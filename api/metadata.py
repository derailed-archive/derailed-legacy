# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


import os
import typing

import asyncpg

__all__ = ("Meta", "Object", "meta")


class Meta:
    def __init__(self) -> None:
        self.cache: dict[str, Object] = {}

    async def initialize(self) -> None:
        self.db = asyncpg.create_pool(os.environ["DATABASE_URL"])


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
