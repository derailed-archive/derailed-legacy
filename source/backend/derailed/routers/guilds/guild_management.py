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
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from ...database import AsyncSession, to_dict, uses_db
from ...identification import medium, version
from ...models.guild import Guild
from ...models.member import Member
from ...models.user import User
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
    guild = Guild(
        id=medium.snowflake(),
        name=data.name,
        owner_id=user.id,
        flags=0,
        permissions=DEFAULT_PERMISSIONS,
    )
    session.add(guild)
    member = Member(user_id=user.id, guild_id=guild.id, nick=None)
    session.add(member)

    await session.commit()

    prepare_default_channels(guild, session)

    await session.commit()

    await publish_to_user(user_id=user.id, event='GUILD_CREATE', data=to_dict(guild))

    return to_dict(guild)


class ModifyGuild(BaseModel):
    name: str | Undefined = Field(UNDEFINED, min_length=1, max_length=30)


@version('/guilds/{guild_id}', 1, router, 'PATCH')
async def modify_guild(
    request: Request, guild_id: int, data: CreateGuild, session: AsyncSession = Depends(uses_db)
) -> None:
    guild, member = await prepare_membership(guild_id)

    if not data.name:
        return to_dict(guild)

    await prepare_permissions(member, guild, [GuildPermissions.MODIFY_GUILD])

    guild.name = data.name

    session.add(guild)

    await session.commit()

    await publish_to_guild(guild.id, 'GUILD_UPDATE', to_dict(guild))

    return to_dict(guild)
