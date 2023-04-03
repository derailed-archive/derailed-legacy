# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

import functools
import weakref
from enum import Enum, auto
from typing import Literal

import async_lru


def memo(*lru_args, **lru_kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(self, *args, **kwargs):
            self_weak = weakref.ref(self)

            @functools.wraps(func)
            @async_lru.alru_cache(*lru_args, lru_kwargs)
            async def cached_method(*args, **kwargs):
                return await func(self_weak(), *args, **kwargs)

            setattr(self, func.__name__, cached_method)

            return cached_method(*args, **kwargs)

        return wrapped_func

    return decorator


class Missing(Enum):
    MISSING = auto()


MISSING: Literal[Missing.MISSING] = Missing.MISSING
