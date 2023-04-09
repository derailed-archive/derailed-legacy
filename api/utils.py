# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

from enum import Enum, auto
from typing import Literal, TypeVar, Union

T = TypeVar("T")


class Missing(Enum):
    MISSING = auto()

    def __bool__(self) -> Literal[False]:
        return False


MISSED: Literal[Missing.MISSING] = Missing.MISSING

MISSING = Union[T, Missing]
