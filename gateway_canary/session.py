# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

import asyncio
import random

import msgspec
import pydantic
import ulid
from falcon import WebSocketDisconnected
from falcon.asgi import WebSocket

from .stream import stream

from ..api.models.settings import Settings
from .models import Activity, Guild, Member, ReadState
from .payloads import Base, GetMembers, HeartbeatResponse, Identify, UpdatePresence
from .utils import MISSING, Maybe, bulk_publish, presences, subscriptions, tokenizer


class Session:
    def __init__(self, ws: WebSocket, version: str, transport: str) -> None:
        self._ws = ws
        self.version = version
        self.transport = transport
        self.heartbeat_interval = random.randint(45, 48)
        self.identified = False
        self.hb_id = None

    async def process_type(self, t: str, data: dict) -> None:
        # TODO: handle PRESENCE_UPDATE from secondary connections
        match t:
            case "GUILD_CREATE":
                self.guild_ids.append(int(data["id"]))
                sub = subscriptions.get(int(data["id"]))

                if sub:
                    subscriptions[int(data["id"])].append(self)
                else:
                    subscriptions[int(data["id"])] = [self]

            case "GUILD_DELETE":
                self.guild_ids.remove(int(data["id"]))

                sub = subscriptions.get(int(data["id"]))

                if sub:
                    subscriptions[int(data["id"])].remove(self)
            case "USER_DELETE":
                await self._ws.close(5006)

    async def send(self, job: int, d: dict, t: Maybe[str] = MISSING) -> None:
        data = {"j": job, "d": d}

        if t:
            data["t"] = t
            asyncio.create_task(self.process_type(t, d))

        binary = msgspec.msgpack.encode(data)

        await self._ws.send_data(binary)

    async def _recv(self) -> None:
        while True:
            try:
                data = await self._ws.receive_data()
                asyncio.create_task(self.initial_recv(data))
            except WebSocketDisconnected:
                break

    async def initial_recv(self, data: bytes) -> None:
        try:
            dec = msgspec.msgpack.decode(data, type=dict)
        except msgspec.DecodeError:
            await self._ws.close(5001)
            return

        try:
            base = Base.validate(dec)
        except pydantic.ValidationError:
            await self._ws.close(5001)
            return

        match base.op:
            case 1:
                await self.identify(base.d)
            case 3:
                await self.update_presence(base.d)
            case 4:
                await self.get_guild_members(base.d)
            case 8:
                await self.heartbeat_response(base.d)

    async def identify(self, data: dict) -> None:
        if self.identified:
            await self._ws.close(5003)
            return

        try:
            identity = Identify.validate(data)
        except pydantic.ValidationError:
            await self._ws.close(5001)
            return

        try:
            user = await tokenizer(identity.token)
        except ValueError:
            await self._ws.close(5002)
            return

        self.client_status = identity.client_status
        self.user_id = user.id

        settings = await user.get_settings()
        read_states = await ReadState.acquire_all(user.id)
        members = await Member.acquire_all(user.id)
        guilds = [await Guild.acquire(member.guild_id) for member in members]
        activities = await Activity.acquire_all(user.id)
        guild_ids = [guild.id for guild in guilds]

        acts = [await activity.publicize() for activity in activities]

        presence = {
            "user_id": str(user.id),
            "status": settings.status,
            "activities": acts,
        }

        if self.client_status in ["desktop", "mobile"]:
            presence["client_status"] = self.client_status

        await self.send(
            5,
            {
                "v": "1",
                "transport": "msgpack",
                "user": await user.publicize(secure=True),
                "settings": await settings.publicize(),
                "read_states": [await rds.publicize() for rds in read_states],
                "guilds": [await guild.publicize() for guild in guilds],
                "members": [await member.publicize() for member in members],
                "activities": acts,
            },
        )

        # TODO: dm channels
        await bulk_publish(guild_ids, presence, "PRESENCE_UPDATE")

        if subscriptions.get(self.user_id):
            subscriptions[self.user_id].append(self)
        else:
            subscriptions[self.user_id] = [self]

        for guild_id in guild_ids:
            pres = presences.get(guild_id)

            if pres and self.user_id not in pres["user_ids"]:
                presences[guild_id]["count"] += 1
            elif not pres:
                presences[guild_id] = {"count": 1, "user_ids": [self.user_id]}

        self.guild_ids = guild_ids


    async def update_presence(self, data: dict) -> None:
        if not self.identified:
            await self._ws.close(5004)
            return

        try:
            update = UpdatePresence.validate(data)
        except pydantic.ValidationError:
            await self._ws.close(5001)
            return

        await Activity.delete(self.user_id)

        acts = []

        for activity in update.activities:
            act = await Activity.create(self.user_id, activity.type, activity.content)
            acts.append(await act.publicize())

        settings = await Settings.acquire(self.user_id)
        settings.status = update.status
        await settings.modify()

        presence = {
            "user_id": str(self.user_id),
            "status": settings.status,
            "activities": acts,
        }

        if self.client_status in ["desktop", "mobile"]:
            presence["client_status"] = self.client_status

        await bulk_publish(self.guild_ids, presence, "PRESENCE_UPDATE")

    async def get_guild_members(self, data: dict) -> None:
        if not self.identified:
            await self._ws.close(5004)
            return

        try:
            guild_info = GetMembers.validate(data)
        except pydantic.ValidationError:
            await self._ws.close(5001)
            return

        guild_id = guild_info.guild_id

        if guild_id not in self.guild_ids:
            await self._ws.close(5005)
            return

        members = await Member.acquire_guild(guild_id)

        await self.send(
            6,
            {
                "guild_id": guild_id,
                "members": [await member.publicize() for member in members],
            },
        )

    async def _hb_repeat(self) -> None:
        await asyncio.sleep(self.heartbeat_interval)

        self.hb_responded = False
        self.hb_id = str(ulid.new().hex)

        try:
            await self.send(7, {"id": self.hb_id})
        except WebSocketDisconnected:
            return

        asyncio.create_task(self._hb_wait())
        asyncio.create_task(self._hb_repeat())

    async def _hb_wait(self) -> None:
        await asyncio.sleep(random.randint(4, 8))

        if not self.hb_responded:
            await self._ws.close(5009)

    async def heartbeat_response(self, data: dict) -> None:
        if not self.identified:
            await self._ws.close(5004)
            return

        if self.hb_responded is True or self.hb_id is None:
            await self._ws.close(5007)
            return

        try:
            hb_info = HeartbeatResponse.validate(data)
        except pydantic.ValidationError:
            await self._ws.close(5001)
            return

        if self.hb_id != hb_info.id:
            await self._ws.close(5008)
            return
        else:
            self.hb_responded = True

    async def start(self) -> None:
        await stream.start()
        self.session_id = str(ulid.new().hex)

        await self.send(2, {"heartbeat_interval": self.heartbeat_interval})
        asyncio.create_task(self._hb_repeat())

        await self._recv()

        if self.identified:
            presence = {
                "user_id": str(self.user_id),
                "status": 1,
                "activities": [],
            }

            for guild_id in self.guild_ids:
                sub = subscriptions.get(guild_id)

                if sub:
                    subscriptions[guild_id].remove(self)

            del subscriptions[self.user_id]

            await bulk_publish(self.guild_ids, presence, "PRESENCE_UPDATE")
