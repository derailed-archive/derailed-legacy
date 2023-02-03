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

if os.name != 'nt':
    import asyncio

    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from .models.base import Base
from .database import engine

# routers
from .routers import user
from .routers.channels import guild_channel, message
from .routers.guilds import guild_information, guild_management, invites

app = FastAPI(version='1')
app.include_router(user.router)
app.include_router(guild_information.router)
app.include_router(guild_management.router)
app.include_router(guild_channel.router)
app.include_router(message.router)
app.include_router(invites.router)


@app.on_event('startup')
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
