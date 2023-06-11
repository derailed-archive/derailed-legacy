# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

# TODO: distribute presences

from typing import Any

# guild_id: {user_id: presence}
presences: dict[int, dict[str, Any]] = {}
