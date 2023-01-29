"""
Copyright (C) 2021-2023 Derailed.

Under no circumstances may you publicly share, distribute, or give any objects, files, or media in this project.
You may only share the above with individuals who have permission to view these files already.
If they don't have permission but are still given the files, or if code is shared publicly, 
we have the legal jurisdiction to bring forth charges under which is owed, based in the damages.

You may under some circumstances with authorized permission share snippets of the code for specific reasons.
Any media and product here must be kept proprietary unless otherwise necessary or authorized.
"""
import os
from datetime import datetime
from inspect import isbuiltin, isfunction, ismethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine(
    os.environ['PG_URI'],
    future=True,
)


AsyncSessionFactory = async_sessionmaker(
    engine, autoflush=True, expire_on_commit=False, autobegin=True
)


async def uses_db():
    session = AsyncSessionFactory()
    try:
        yield session
    except:
        await session.rollback()
    finally:
        await session.close()


def get_db() -> AsyncSession:
    session: AsyncSession = AsyncSessionFactory()
    return session


def to_dict(self) -> dict[str, Any]:
    if isinstance(self, list):
        return [to_dict(obj) for obj in self]

    d = {}
    for k in dir(self):
        if k == '__dict__':
            continue

        attr = getattr(self, k)

        if (
            not isfunction(attr)
            and k not in ['registry', 'mro', 'metadata']
            and not k.startswith('_')
            and not ismethod(attr)
            and not isbuiltin(attr)
        ):
            d[k] = attr

            if isinstance(attr, int):
                if attr > 2_147_483_647:
                    d[k] = str(attr)
            elif isinstance(attr, datetime):
                d[k] = attr.isoformat()
    return d
