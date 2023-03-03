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
import re

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import to_dict, uses_db
from ...identification import medium, version
from ...models.channel import Message
from ...models.user import User
from ...permissions import GuildPermissions
from ...powerbase import (
    MESSAGE_MENTION_REGEX,
    abort_forb,
    prepare_channel,
    prepare_membership,
    prepare_message,
    prepare_permissions,
    publish_to_guild,
    uses_auth,
)
from ...undefinable import UNDEFINED, Undefined

router = APIRouter()


def length_message(text):
    # Replace mentions with a single character
    text = re.sub(MESSAGE_MENTION_REGEX, 'X', text)
    # Replace tabs with nothing
    text = text.replace('\n', '')
    return len(text)



@version('/channels/{channel_id}/messages', 1, router, 'GET')
async def get_messages(
    channel_id: int,
    request: Request,
    limit: int = Query(50, gt=0, lt=100),
    session: AsyncSession = Depends(uses_db),
    user: User = Depends(uses_auth),
) -> None:
    channel = await prepare_channel(session, int(channel_id))

    if channel.guild_id is not None:
        guild, member = await prepare_membership(channel.guild_id, user, session)

        prepare_permissions(member, guild, required=[GuildPermissions.VIEW_MESSAGE_HISTORY.value])
    else:
        if user not in channel.members:
            raise HTTPException(403, 'You are forbidden from this channel')

    messages = await Message.sorted_channel(session, channel, limit)

    return prepare_message(messages)


@version('/channels/{channel_id}/messages/{message_id}', 1, router, 'GET')
async def get_message(
    channel_id: int,
    request: Request,
    message_id: int,
    session: AsyncSession = Depends(uses_db),
    user: User = Depends(uses_auth),
) -> None:
    channel = await prepare_channel(session, channel_id)

    if channel.guild_id is not None:
        guild, member = await prepare_membership(channel.guild_id, user, session)

        prepare_permissions(member, guild, required=[GuildPermissions.VIEW_MESSAGE_HISTORY.value])
    else:
        if user not in channel.members:
            raise HTTPException(403, 'You are forbidden from this channel')

    message = await Message.get(session, message_id, channel)

    if message is None:
        raise HTTPException(404, 'Message not found')

    return prepare_message(message)


class CreateMessage(BaseModel):
    content: str = Field(min_length=1, max_length=1700)


@version('/channels/{channel_id}/messages', 1, router, 'POST', status_code=201)
async def create_message(
    data: CreateMessage,
    request: Request,
    channel_id: int,
    session: AsyncSession = Depends(uses_db),
    user: User = Depends(uses_auth),
) -> None:
    if length_message(data) > 1024:
        raise HTTPException(400, 'Message content must be or must be under 1024')

    channel = await prepare_channel(session, channel_id)

    if channel.guild_id is not None:
        guild, member = await prepare_membership(channel.guild_id, user, session)

        prepare_permissions(member, guild, required=[GuildPermissions.VIEW_MESSAGE_HISTORY.value])
    else:
        if user not in channel.members:
            raise HTTPException(403, 'You are forbidden from this channel')

    mid = medium.snowflake()
    message = Message(
        id=mid,
        author_id=user.id,
        content=data.content,
        channel_id=channel.id,
        timestamp=datetime.now(),
        edited_timestamp=None,
    )

    session.add(message)
    await session.commit()

    channel.last_message_id = message.id

    session.add(channel)
    await session.commit()

    if channel.guild_id is not None:
        publish_to_guild(channel.guild_id, 'MESSAGE_CREATE', to_dict(message))

    return prepare_message(message)


class ModifyMessage(BaseModel):
    content: str | Undefined = Field(UNDEFINED, max_length=1, min_length=1024)


@version('/channels/{channel_id}/messages/{message_id}', 1, router, 'PATCH')
async def edit_message(
    data: ModifyMessage,
    request: Request,
    channel_id: int,
    message_id: int,
    session: AsyncSession = Depends(uses_db),
    user: User = Depends(uses_auth),
) -> None:
    channel = await prepare_channel(session, channel_id)

    message = await Message.get(session, message_id, channel)

    if message is None:
        raise HTTPException(404, 'Message does not exist')

    if message.author_id != user.id:
        abort_forb()

    message.content = data.content

    session.add(message)
    await session.commit()

    if channel.guild_id is not None:
        publish_to_guild(channel.guild_id, 'MESSAGE_EDIT', to_dict(message))

    return prepare_message(message)


@version(
    '/channels/{channel_id}/messages/{message_id}', 1, router, 'DELETE', status_code=204
)
async def delete_message(
    channel_id: int,
    message_id: int,
    request: Request,
    session: AsyncSession = Depends(uses_db),
    user: User = Depends(uses_auth),
) -> None:
    channel = await prepare_channel(session, channel_id)

    message = await Message.get(session, message_id, channel)

    if message is None:
        raise HTTPException(404, 'Message does not exist')

    if message.author_id == user.id:
        await message.delete(session, message.id)
        return ''

    if channel.guild_id is not None:
        guild, member = await prepare_membership(channel['guild_id'], user, session)

        prepare_permissions(member, guild, required=[GuildPermissions.MODIFY_MESSAGES.value])

    await message.delete(session, message.id)

    if channel.guild_id is not None:
        publish_to_guild(
            channel.guild_id,
            'MESSAGE_DELETE',
            {
                'message_id': str(message_id),
                'guild_id': str(channel.guild_id),
                'channel_id': str(channel.id),
            },
        )

    return ''
