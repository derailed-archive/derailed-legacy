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
from time import time

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
async def get_guild(request: Request, md: tuple[Guild, Member] = Depends(prepare_membership)) -> None:
    return to_dict(md[0])
