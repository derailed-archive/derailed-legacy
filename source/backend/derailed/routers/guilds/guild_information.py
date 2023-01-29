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
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import to_dict, uses_db
from ...identification import version
from ...models.guild import Guild
from ...models.member import Member
from ...powerbase import get_guild_info, prepare_guild, prepare_membership

router = APIRouter()


@version('/guilds/{guild_id}/preview', 1, router, 'GET')
async def get_guild_preview(
    request: Request, guild_id: int, session: AsyncSession = Depends(uses_db)
) -> None:
    guild = await prepare_guild(session, guild_id)

    guild_info = await get_guild_info(str(guild_id))

    gid = to_dict(guild)
    gid['approximate_presence_count'] = guild_info.presences
    gid['available'] = guild_info.available

    return gid


@version('/guilds/{guild_id}', 1, router, 'GET')
async def get_guild(
    request: Request, md: tuple[Guild, Member] = Depends(prepare_membership)
) -> None:
    return to_dict(md[0])
