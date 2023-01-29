"""
Copyright (C) 2021-2023 Derailed.

Under no circumstances may you publicly share, distribute, or give any objects, files, or media in this project.
You may only share the above with individuals who have permission to view these files already.
If they don't have permission but are still given the files, or if code is shared publicly, 
we have the legal jurisdiction to bring forth charges under which is owed, based in the damages.

You may under some circumstances with authorized permission share snippets of the code for specific reasons.
Any media and product here must be kept proprietary unless otherwise necessary or authorized.
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

