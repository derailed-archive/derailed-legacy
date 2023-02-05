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

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import uses_db

from ...powerbase import uses_auth

from ...models.user import User
from ...identification import version
from ...models import ReadState


router = APIRouter()


@version('/readstates', 1, router, 'GET')
async def get_readstates(user: User = Depends(uses_auth), session: AsyncSession = Depends(uses_db)) -> None:
    readstates = await ReadState.get_all(session, user.id)

    return readstates

