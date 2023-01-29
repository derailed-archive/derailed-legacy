"""
Copyright (C) 2021-2023 Derailed.

Under no circumstances may you publicly share, distribute, or give any objects, files, or media in this project.
You may only share the above with individuals who have permission to view these files already.
If they don't have permission but are still given the files, or if code is shared publicly, 
we have the legal jurisdiction to bring forth charges under which is owed, based in the damages.

You may under some circumstances with authorized permission share snippets of the code for specific reasons.
Any media and product here must be kept proprietary unless otherwise necessary or authorized.
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
