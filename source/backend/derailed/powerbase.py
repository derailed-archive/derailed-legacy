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
import asyncio
import base64
import binascii
import json
import math
import os
import re
from typing import Any, NoReturn

import grpc.aio as grpc
from fastapi import Depends, HTTPException, Path, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db, to_dict, uses_db
from .grpc import derailed_pb2_grpc
from .grpc.auth import auth_pb2_grpc
from .grpc.auth.auth_pb2 import CreateToken, NewToken, Valid, ValidateToken
from .grpc.derailed_pb2 import GetGuildInfo, Message, Publ, RepliedGuildInfo, UPubl
from .identification import medium
from .models import Channel, Guild, Member, User
from .models.channel import ChannelType
from .permissions import (
    GuildPermission,
    has_bit,
    merge_permissions,
    unwrap_guild_permissions,
)


MESSAGE_MENTION_REGEX = re.compile(r'(@here|@everyone|<@(\d+)>|<@&(\d+)>|<#(\d+)>)')


async def uses_auth(request: Request, session: AsyncSession = Depends(uses_db)) -> User:
    token = request.headers.get('Authorization', None)

    if token is None or token == '':
        abort_auth()

    splits = token.split('.')

    try:
        user_id = splits[0]
        user_id = base64.urlsafe_b64decode(user_id).decode()
    except (binascii.Error, UnicodeDecodeError, IndexError):
        abort_auth()

    user = await User.get(session, int(user_id))

    if user is None:
        abort_auth()

    is_valid = await valid_authorization(user_id, user.password, token)

    if is_valid is False:
        abort_auth()

    return user


async def uses_no_raises_auth(
    request: Request, session: AsyncSession = Depends(uses_db)
) -> User | None:
    token = request.headers.get('Authorization', None)

    if token is None or token == '':
        return None

    splits = token.split('.')

    try:
        user_id = splits[0]
        user_id = base64.urlsafe_b64decode(user_id).decode()
    except (binascii.Error, UnicodeDecodeError, IndexError):
        return None

    user = await User.get(session, int(user_id))

    if user is None:
        return None

    is_valid = await valid_authorization(user_id, user.password, token)

    if is_valid is False:
        return None

    return user


async def get_key(request: Request) -> str:
    """
    Gets the rate limit key for this request
    """
    session = get_db()

    user = await uses_no_raises_auth(request, session)

    if user:
        return str(user.id)
    else:
        # TODO
        return ''


async def default_callback(request: Request, response: Response, pexpire: int):
    """
    default callback when too many requests
    :param request:
    :param pexpire: The remaining milliseconds
    :param response:
    :return:
    """
    expire = math.ceil(pexpire / 1000)

    raise HTTPException(429, {'type': 'rate_limited', 'retry_after': expire})


def prepare_user(user: User, own: bool = False) -> dict[str, Any]:
    user = to_dict(user)

    if not own:
        user.pop('email')

    user.pop('password', None)
    user.pop('deletor_job_id', None)
    return user


def abort_auth() -> NoReturn:
    raise HTTPException(401, 'Invalid Authorization')


def abort_forb() -> NoReturn:
    raise HTTPException(403, 'Forbidden')


user_stub = None
guild_stub = None
auth_stub = None


async def _init_stubs() -> None:
    global user_stub
    global guild_stub
    global auth_stub
    user_channel = grpc.insecure_channel(os.environ['USER_CHANNEL'])
    user_stub = derailed_pb2_grpc.UserStub(user_channel)
    guild_channel = grpc.insecure_channel(os.environ['GUILD_CHANNEL'])
    guild_stub = derailed_pb2_grpc.GuildStub(guild_channel)
    auth_channel = grpc.insecure_channel(os.environ['AUTH_CHANNEL'])
    auth_stub = auth_pb2_grpc.AuthorizationStub(auth_channel)


def publish_to_user(user_id: Any, event: str, data: dict[str, Any]) -> None:
    asyncio.create_task(_pub_user(user_id, event, data))


async def _pub_user(user_id, event, data) -> None:
    if user_stub is None:
        await _init_stubs()

    await user_stub.publish(
        UPubl(
            user_id=str(user_id),
            message=Message(event=event, data=json.dumps(dict(data))),
        )
    )


def publish_to_guild(guild_id: Any, event: str, data: dict[str, Any]) -> None:
    asyncio.create_task(_pub_guild(guild_id, event, data))


async def _pub_guild(guild_id, event, data) -> None:
    if guild_stub is None:
        await _init_stubs()

    await guild_stub.publish(
        Publ(
            guild_id=str(guild_id),
            message=Message(event=event, data=json.dumps(dict(data))),
        )
    )


async def get_guild_info(guild_id: int) -> RepliedGuildInfo:
    if guild_stub is None:
        await _init_stubs()

    return await guild_stub.get_guild_info(GetGuildInfo(guild_id=str(guild_id)))


async def create_token(user_id: str | int, password: str) -> str:
    if auth_stub is None:
        await _init_stubs()

    # stringify user_id just in case it isn't already
    req: NewToken = await auth_stub.create(
        CreateToken(user_id=str(user_id), password=password)
    )

    return req.token


async def valid_authorization(user_id: str, password: str, token: str) -> bool:
    if auth_stub is None:
        await _init_stubs()

    req: Valid = await auth_stub.validate(
        ValidateToken(user_id=user_id, password=password, token=token)
    )

    return req.valid


async def prepare_guild(session: AsyncSession, guild_id: int) -> Guild:
    guild = await Guild.get(session, guild_id)

    if guild is None:
        raise HTTPException(404, 'Guild not found')

    return guild


async def prepare_membership(
    guild_id: int = Path(),
    user: User = Depends(uses_auth),
    session: AsyncSession = Depends(uses_db),
) -> tuple[Guild, Member]:
    guild = await prepare_guild(session, guild_id)

    member = await Member.get(session, user.id, guild.id)

    if member is None:
        abort_forb()

    return (guild, member)


def prepare_permissions(
    member: Member, guild: Guild, required_permissions: list[int]
) -> None:
    if guild.owner_id == member.user_id:
        return

    roles = member.roles
    permsl: list[GuildPermission] = []

    for role in roles:
        permsl.append(
            unwrap_guild_permissions(
                allow=role.permissions.allow,
                deny=role.permissions.deny,
                pos=role.position,
            )
        )

    perms = merge_permissions(*permsl)

    for perm in required_permissions:
        if not has_bit(perms, perm):
            raise HTTPException(403, 'Invalid permissions')


CHANNEL_REGEX = '^[a-z0-9](?:[a-z0-9-_]{1,32}[a-z0-9])?$'


async def prepare_channel_position(
    session: AsyncSession, wanted_position: int, parent_id: int | None, guild: Guild
) -> None:
    c = await Channel.get_for_pos(session, wanted_position, guild.id, parent_id)

    if c is None:
        return

    guild_channels = await Channel.get_via(session, parent_id, guild.id)

    for channel in guild_channels:
        if channel.position >= wanted_position:
            channel.position += 1
            session.add(channel)

    await session.commit()


async def prepare_category_position(
    session: AsyncSession, wanted_position: int, guild: Guild
) -> None:
    c = await Channel.get_for_pos(session, wanted_position, guild.id)

    if c is None:
        return

    guild_channels = await Channel.get_via(session, None, guild.id)

    for channel in guild_channels:
        if channel.type != ChannelType.CATEGORY:
            continue

        if channel.position >= wanted_position:
            channel.position += 1
            session.add(channel)

    await session.commit()


async def prepare_guild_channel(
    session: AsyncSession, channel_id: int, guild: Guild
) -> Channel:
    channel_id = str(channel_id)

    channel = await Channel.get(session, channel_id, guild.id)

    if channel is None:
        raise HTTPException(404, 'Channel not found')

    return channel


async def prepare_channel(session: AsyncSession, channel_id: int) -> Channel:
    channel_id = str(channel_id)

    channel = await Channel.get(session, channel_id)

    if channel is None:
        raise HTTPException(404, 'Channel not found')

    return channel


def prepare_default_channels(guild: Guild, session: AsyncSession) -> None:
    cat = Channel(
        id=medium.snowflake(),
        name='general',
        parent_id=None,
        type=ChannelType.CATEGORY,
        guild_id=guild.id,
        position=1,
    )
    general = Channel(
        id=medium.snowflake(),
        name='general',
        parent_id=cat.id,
        type=ChannelType.TEXT,
        last_message_id=None,
        guild_id=guild.id,
        position=1,
    )

    session.add_all([cat, general])
