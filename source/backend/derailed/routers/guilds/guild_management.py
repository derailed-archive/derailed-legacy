"""
Copyright (C) 2021-2023 Derailed.

Under no circumstances may you publicly share, distribute, or give any objects, files, or media in this project.
You may only share the above with individuals who have permission to view these files already.
If they don't have permission but are still given the files, or if code is shared publicly, 
we have the legal jurisdiction to bring forth charges under which is owed, based in the damages.

You may under some circumstances with authorized permission share snippets of the code for specific reasons.
Any media and product here must be kept proprietary unless otherwise necessary or authorized.
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
    request: Request,
    guild_id: int,
    data: CreateGuild,
    user: User = Depends(uses_auth),
    session: AsyncSession = Depends(uses_db),
) -> None:
    guild, member = await prepare_membership(guild_id, user, session)

    if not data.name:
        return to_dict(guild)

    prepare_permissions(member, guild, [GuildPermissions.MODIFY_GUILD])

    guild.name = data.name

    session.add(guild)

    await session.commit()

    await publish_to_guild(guild.id, 'GUILD_UPDATE', to_dict(guild))

    return to_dict(guild)
