# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from enum import IntFlag


class RolePermissions(IntFlag):
    ADMINISTRATOR = 0
    VIEW_CHANNELS = 1
    MANAGE_CHANNELS = 2
    VIEW_MESSAGE_HISTORY = 3
    MANAGE_GUILD = 4
    SEND_MESSAGES = 5
    MANAGE_MESSAGES = 6
    MANAGE_ROLES = 7
    MANAGE_MEMBERS = 8
    MANAGE_NICKNAMES = 9
    MANAGE_INVITES = 10
    CREATE_INVITES = 11
    MANAGE_BANS = 12
    KICK_MEMBERS = 13
    MENTION_EVERYONE = 14


class UserFlags(IntFlag):
    staff = 0
    bot = 1
    early_user = 2
    original_tester = 3
    mod = 4


DEFAULT_FLAGS = UserFlags.early_user | UserFlags.original_tester


DEFAULT_PERMISSIONS = (
    RolePermissions.VIEW_MESSAGE_HISTORY
    | RolePermissions.VIEW_CHANNELS
    | RolePermissions.SEND_MESSAGES
    | RolePermissions.CREATE_INVITES
    | RolePermissions.MENTION_EVERYONE
)
