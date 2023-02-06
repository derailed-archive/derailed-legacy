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
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import to_dict, uses_db
from ...identification import medium, version
from ...models import Invite
from ...models.channel import Channel
from ...models.guild import Guild
from ...models.member import Member
from ...models.user import GuildPosition, User
from ...permissions import GuildPermissions
from ...powerbase import (
    prepare_membership,
    prepare_permissions,
    publish_to_guild,
    publish_to_user,
    uses_auth,
)

router = APIRouter()


@version('/invites/{invite_id}', 1, router, 'GET')
async def get_invite(invite_id: str, session: AsyncSession = Depends(uses_db)) -> None:
    invite = await Invite.get(session, invite_id)

    if invite is None:
        raise HTTPException(404, 'Invite not found')

    inv = to_dict(invite)
    inv.pop('guild_id')
    inv.pop('channel_id')
    inv['guild'] = to_dict(await Guild.get(session, invite.guild_id))
    inv['channel'] = to_dict(
        await Channel.get(session, invite.channel_id, invite.guild_id)
    )

    return inv


@version('/invites/{invite_id}', 1, router, 'POST')
async def join_guild(
    invite_id: str,
    user: User = Depends(uses_auth),
    session: AsyncSession = Depends(uses_db),
) -> None:
    invite = await Invite.get(session, invite_id)

    if invite is None:
        raise HTTPException(404, 'Invite not found')

    guild = await Guild.get(session, invite.guild_id)

    guild_positions = await GuildPosition.get_for(session, user)

    # TODO: proper search in the db
    for guild_pos in guild_positions:
        if guild_pos.guild_id == guild.id:
            raise HTTPException(403, 'Already joined this Guild')

    new_guild_pos = await GuildPosition.for_new(session, user.id)

    member = Member(user_id=user.id, guild_id=guild.id, nick=None)
    guild_position = GuildPosition(
        user_id=user.id, guild_id=guild.id, position=new_guild_pos
    )

    session.add_all([member, guild_position])
    await session.commit()

    publish_to_guild(invite.guild_id, 'MEMBER_JOIN', to_dict(member))
    publish_to_user(user.id, 'GUILD_CREATE', to_dict(guild))

    return {'member': to_dict(member), 'guild': to_dict(guild)}


@version(
    '/guilds/{guild_id}/channels/{channel_id}/invites', 1, router, 'POST', status_code=201
)
async def create_invite(
    guild_id: int,
    channel_id: int,
    user: User = Depends(uses_auth),
    session: AsyncSession = Depends(uses_db),
) -> None:
    guild, member = await prepare_membership(guild_id, user, session)

    prepare_permissions(member, guild, required=[GuildPermissions.CREATE_INVITES.value])

    # TODO: maybe make 10 not a hard limit
    for _ in range(10):
        invite_id = medium.invite()

        inv = Invite.get(session, invite_id)

        if inv is not None:
            invite_id = None
            continue
        else:
            break

    if invite_id is None:
        raise HTTPException(400, 'Unable to retrieve unique id')

    invite = Invite(
        id=invite_id, guild_id=guild_id, channel_id=channel_id, author_id=user.id
    )

    session.add(invite)
    await session.commit()

    return to_dict(invite)


@version('/guilds/{guild_id}/invites/{invite_id}', 1, router, 'DELETE', status_code=204)
async def delete_invite(
    guild_id: int,
    invite_id: int,
    user: User = Depends(uses_auth),
    session: AsyncSession = Depends(uses_db),
) -> None:
    guild, member = await prepare_membership(guild_id, user, session)

    invite = await Invite.get(session, invite_id)

    if invite is None:
        raise HTTPException(404, 'Invite not found')
    elif invite.guild_id != guild.id:
        raise HTTPException(404, 'Incorrect Invite Guild')

    # to avoid any legal bs
    if invite.author_id == member.user_id:
        await session.delete(invite)
        await session.commit()
        return ''

    prepare_permissions(member, guild, required=[GuildPermissions.MODIFY_INVITES.value])

    await session.delete(invite)
    await session.commit()
    return ''
