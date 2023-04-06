# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

from enum import Enum, auto
from typing import Literal


class Missing(Enum):
    MISSING = auto()


MISSING: Literal[Missing.MISSING] = Missing.MISSING
