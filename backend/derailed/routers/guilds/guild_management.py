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
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from ...database import AsyncSession, to_dict, uses_db
from ...identification import medium, version
from ...models.guild import Guild
from ...models.member import Member
from ...models.user import GuildPosition, User
from ...permissions import DEFAULT_PERMISSIONS, GuildPermissions
from ...powerbase import (
    prepare_default_channels,
    prepare_membership,
    prepare_permissions,
    publish_to_guild,
    publish_to_user,
    uses_auth,
)
from ...undefinable import UNDEFINED, Undefined

router = APIRouter()


class CreateGuild(BaseModel):
    name: str = Field(min_length=1, max_length=32)


@version('/guilds', 1, router, 'POST', status_code=201)
async def create_guild(
    request: Request,
    data: CreateGuild,
    session: AsyncSession = Depends(uses_db),
    user: User = Depends(uses_auth),
) -> None:
    new_guild_position = await GuildPosition.for_new(session, user.id)

    guild = Guild(
        id=medium.snowflake(),
        name=data.name,
        owner_id=user.id,
        flags=0,
        permissions=DEFAULT_PERMISSIONS,
    )
    session.add(guild)
    guild_position = GuildPosition(
        user_id=user.id, guild_id=guild.id, position=new_guild_position
    )
    member = Member(user_id=user.id, guild_id=guild.id, nick=None)
    session.add_all([guild_position, member])

    await session.commit()

    await prepare_default_channels(guild, session)

    publish_to_user(user_id=user.id, event='GUILD_CREATE', data=to_dict(guild))

    return to_dict(guild)


class ModifyGuild(BaseModel):
    name: str | Undefined = Field(UNDEFINED, min_length=1, max_length=30)


@version('/guilds/{guild_id}', 1, router, 'PATCH')
async def modify_guild(
    request: Request,
    guild_id: int,
    data: CreateGuild,
    user: User = Depends(uses_auth),
    session: AsyncSession = Depends(uses_db),
) -> None:
    guild, member = await prepare_membership(guild_id, user, session)

    if not data.name:
        return to_dict(guild)

    prepare_permissions(member, guild, required=[GuildPermissions.MODIFY_GUILD])

    guild.name = data.name

    session.add(guild)

    await session.commit()

    publish_to_guild(guild.id, 'GUILD_UPDATE', to_dict(guild))

    return to_dict(guild)
