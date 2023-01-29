"""
Copyright (C) 2021-2023 Derailed.

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
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import to_dict, uses_db
from ...identification import medium, version
from ...models.channel import Channel, ChannelType
from ...models.user import User
from ...permissions import GuildPermissions
from ...powerbase import (
    CHANNEL_REGEX,
    prepare_category_position,
    prepare_channel_position,
    prepare_guild_channel,
    prepare_membership,
    prepare_permissions,
    publish_to_guild,
    uses_auth,
)
from ...undefinable import UNDEFINED, Undefined

router = APIRouter()


@version('/guilds/{guild_id}/channels/{channel_id}', 1, router, 'GET')
async def get_channel(
    guild_id: int,
    channel_id: int,
    request: Request,
    session: AsyncSession = Depends(uses_db),
    user: User = Depends(uses_auth),
) -> None:
    guild, member = await prepare_membership(guild_id, user, session)

    channel = await prepare_guild_channel(session, channel_id, guild)

    prepare_permissions(member, guild, [GuildPermissions.VIEW_CHANNEL.value])

    return channel


@version('/guilds/{guild_id}/channels', 1, router, 'GET')
async def get_channels(
    guild_id: int, request: Request, session: AsyncSession = Depends(uses_db), user: User = Depends(uses_auth)
) -> None:
    guild, _ = await prepare_membership(guild_id, user, session)

    # TODO: check permissions
    channels = await Channel.get_all(session, guild.id)

    return to_dict(channels)


class CreateChannel(BaseModel):
    type: ChannelType
    name: str = Field(regex=CHANNEL_REGEX)
    position: int | Undefined = Field(UNDEFINED, gt=0, lt=500)
    parent_id: int | Undefined = Field(UNDEFINED)


@version('/guilds/{guild_id}/channels', 1, router, 'POST', status_code=201)
async def create_channel(
    data: CreateChannel,
    guild_id: int,
    request: Request,
    session: AsyncSession = Depends(uses_db),
    user: User = Depends(uses_auth),
) -> None:
    guild, member = await prepare_membership(guild_id, user, session)

    prepare_permissions(member, guild, [GuildPermissions.CREATE_CHANNELS.value])

    if data.parent_id:
        parent = await Channel.get(session, data.parent_id, guild_id)

        if parent is None:
            raise HTTPException(400, 'Parent channel does not exist')

        if parent.type != ChannelType.CATEGORY or data.type == ChannelType.CATEGORY:
            raise HTTPException('Parent is not of right type, or child is not of right type')

    channel_count = await Channel.count(session, guild.id)

    if channel_count == 500:
        raise HTTPException(400, 'Max channel count already reached')

    if data.type == 0:
        highest_channel = await Channel.highest(session, guild_id)
    else:
        highest_channel = await Channel.highest(session, guild_id, category=data.parent_id)

    if (highest_channel.position + 1) < data.position and position is not None:
        raise HTTPException(400, 'Channel position too high')
    else:
        position = (highest_channel.position + 1) if data.position is UNDEFINED else data.position

    if data.type == 0:
        await prepare_category_position(session, position, guild)
    else:
        await prepare_channel_position(session, position, data.parent_id, guild)

    channel = Channel(
        id=medium.snowflake(),
        type=data.type,
        parent_id=parent.id,
        name=data.name,
        guild_id=guild_id,
        last_message_id=None,
    )

    session.add(channel)
    await session.commit()

    await publish_to_guild(guild_id, 'CHANNEL_CREATE', to_dict(channel))

    return channel


class ModifyChannel(BaseModel):
    name: str | Undefined = Field(UNDEFINED, regex=CHANNEL_REGEX)
    position: int | Undefined = Field(UNDEFINED, gt=0, lt=500)
    parent_id: int | Undefined = Field(UNDEFINED)


@version('/guilds/{guild_id}/channels/{channel_id}', 1, router, 'PATCH')
async def modify_channel(
    data: ModifyChannel,
    request: Request,
    guild_id: int,
    channel_id: int,
    session: AsyncSession = Depends(uses_db),
    user: User = Depends(uses_auth),
) -> None:
    guild, member = await prepare_membership(guild_id, user, session)

    prepare_permissions(member, guild, [GuildPermissions.MODIFY_CHANNELS.value])

    channel = await prepare_guild_channel(session, channel_id, guild)

    mods = {}

    if data.name:
        mods['name'] = data.name

    if data.parent_id or data.position:
        if channel.type == ChannelType.CATEGORY:
            highest_channel = await Channel.highest(session, guild_id)
        else:
            highest_channel = await Channel.highest(session, guild_id, category=data.parent_id)

    if data.parent_id:
        parent = await Channel.get(session, data.parent_id, guild.id)

        if parent is None or parent.type != ChannelType.CATEGORY or data.type == ChannelType.CATEGORY:
            raise HTTPException(400, 'Parent is not of right type, or child is not of right type')

        await prepare_channel_position(session, highest_channel['position'] + 1, data.parent_id, guild)
        mods['parent_id'] = data.parent_id

    if position:
        if (highest_channel.position + 1) < data.position and position is not None:
            raise HTTPException(400, 'Channel position too high')
        else:
            position = (highest_channel.position + 1) if data.position is UNDEFINED else data.position

        if data.type == 0:
            await prepare_category_position(session, position, guild)
        else:
            await prepare_channel_position(session, position, data.parent_id, guild)
        mods['position'] = position

    await channel.modify(session, **mods)

    await publish_to_guild(guild.id, 'CHANNEL_UPDATE', to_dict(channel))

    return to_dict(channel)


@version('/guilds/{guild_id}/channels/{channel_id}', 1, router, 'DELETE', status_code=204)
async def delete_channel(
    guild_id: int,
    channel_id: int,
    request: Request,
    session: AsyncSession = Depends(uses_db),
    user: User = Depends(uses_auth),
) -> None:
    guild, member = await prepare_membership(guild_id, user, session)

    prepare_permissions(member, guild, [GuildPermissions.MODIFY_CHANNELS.value])

    channel = await prepare_guild_channel(session, channel_id, guild)

    await channel.delete(session)

    await publish_to_guild(guild.id, 'CHANNEL_DELETE', {'channel_id': channel.id, 'guild_id': guild.id})

    return ''
