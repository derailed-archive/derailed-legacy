# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

import asyncio
import random
from typing import Any
import falcon
from falcon.asgi import WebSocket
import msgspec
import pydantic
import ulid

from .schemas import BasicMessage, Identify

from ..api.utils import MISSING, Maybe
from ..api.refs.current_user_ref import CurUserRef
from ..models import User, ReadState, Member, Guild, Activity

class Session:
    def __init__(self, ws: WebSocket) -> None:
        self._ws = ws
        self._sequence = 0
        self.heartbeat_interval = random.randint(45, 48)
        self.identified = False

    async def _receive(self) -> None:
        while True:
            try:
                binary = await self._ws.receive_data()
            except falcon.WebSocketDisconnected:
                break

            asyncio.create_task(self._process(binary))

    async def _process(self, data: bytes) -> None:
        msg = msgspec.json.decode(data, type=dict[str, Any])
        try:
            valid_msg = BasicMessage.validate(msg)
        except pydantic.ValidationError as exc:
            if self.identified:
                await self.send(3, {'_errors': exc.errors})
            else:
                await self._ws.close(5001)
                return

        if valid_msg.j == 1:
            await self.identify(valid_msg.d)

    async def identify(self, data: dict[str, Any]) -> None:
        try:
            iden = Identify.validate(data)
            token = iden.token
        except pydantic.ValidationError:
            await self._ws.close(5001)
            return

        ref = CurUserRef(token)
        user: User = await ref.get_user()

        settings = await user.get_settings()
        read_states = await ReadState.acquire_all(user.id)
        members = await Member.acquire_all(user.id)
        guilds = [await Guild.acquire(member.guild_id) for member in members]
        activities = await Activity.acquire_all(user.id)

        await self.send(1, {
            'v': 1,
            'transport': 'msgpack',
            'user': await user.publicize(secure=True),
            'settings': await settings.publicize(),
            'flags': user.flags,
            'members': [await member.publicize() for member in members],
            'guilds': [await guild.publicize() for guild in guilds],
            'activities': [await activity.publicize() for activity in activities],
            'read_states': [await read_state.publicize() for read_state in read_states],
        })
        self.identified = True


    async def send(self, job: int, d: dict, t: Maybe[str] = MISSING) -> None:
        data = {'j': job, 'd': d}

        if t:
            data['t'] = t

        binary = msgspec.msgpack.encode(data)

        await self._ws.send_data(binary)

    async def start(self) -> None:
        self.session_id = str(ulid.new().hex)

        await self.send(2, {'heartbeat_interval': self.heartbeat_interval})

        await self._receive()
