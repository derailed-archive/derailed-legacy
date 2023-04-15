# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

import functools
import weakref
from enum import Enum, auto
from typing import Literal, TypeVar, Union

import async_lru

T = TypeVar("T")


class Missing(Enum):
    MISSING = auto()

    def __bool__(self) -> Literal[False]:
        return False


MISSING: Literal[Missing.MISSING] = Missing.MISSING

Maybe = Union[T, Missing]


T = TypeVar("T")


def cache() -> T:
    def decorator(func: T):
        @functools.wraps(func)
        def wrapped_func(self, *args, **kwargs):
            self_weak = weakref.ref(self)

            @functools.wraps(func)
            @async_lru.alru_cache()
            async def cached_method(*args, **kwargs):
                return await func(self_weak(), *args, **kwargs)

            setattr(self, func.__name__, cached_method)

            return cached_method(*args, **kwargs)

        return wrapped_func

    return decorator
