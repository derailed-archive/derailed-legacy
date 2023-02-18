"""
Copyright (C) 2021-2023 Derailed

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from enum import IntFlag
from types import SimpleNamespace


def has_bit(value: int, visible: int) -> bool:
    return bool(value & visible)


class GuildPermissions(IntFlag):
    MODIFY_GUILD = 1 << 0
    CREATE_ROLES = 1 << 1
    MODIFY_ROLES = 1 << 2
    CREATE_CHANNELS = 1 << 3
    MODIFY_CHANNELS = 1 << 4
    BAN_MEMBERS = 1 << 5
    MODIFY_MEMBERS = 1 << 6
    KICK_MEMBERS = 1 << 7
    CREATE_MESSAGES = 1 << 8
    MODIFY_MESSAGES = 1 << 9
    VIEW_MESSAGE_HISTORY = 1 << 10
    CREATE_INVITES = 1 << 11
    MODIFY_INVITES = 1 << 12
    ADMINISTRATOR = 1 << 13
    MODIFY_MEMBERS_NICKNAMES = 1 << 14
    VIEW_CHANNEL = 1 << 15


ALL_PERMISSIONS = 0
DEFAULT_PERMISSIONS = 3328

for _v in GuildPermissions:
    ALL_PERMISSIONS += _v.value


class GuildPermission(SimpleNamespace):
    allow: GuildPermissions
    deny: GuildPermissions
    position: int


def unwrap_guild_permissions(
    allow: GuildPermissions, deny: GuildPermissions, pos: int
) -> GuildPermission:
    return GuildPermission(allow=allow, deny=deny, position=pos)


def merge_permissions(*perms: GuildPermission) -> int:
    value: int = 0
    permissions: list[GuildPermission] = []

    for perm in perms:
        permissions.insert(perm.position, perm)

    for perm in permissions:
        if has_bit(perm.allow, GuildPermissions.ADMINISTRATOR.value):
            value = ALL_PERMISSIONS
        elif has_bit(perm.deny, GuildPermissions.ADMINISTRATOR.value):
            value = perm.allow

        for v in GuildPermissions:
            if has_bit(perm.deny, v):
                # denials take hold infront of allows
                value -= v
                continue
            elif has_bit(perm.allow, v):
                value += v

    return value
