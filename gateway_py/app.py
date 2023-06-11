# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


import asyncio
import urllib.parse
from typing import Any
from falcon.asgi import WebSocket, Request

from .session import Session


async def broadcast(message: Any, clients: list) -> None:
    await asyncio.gather(**[client.send_text(message) for client in clients])


class WebSocketResource:
    async def on_get(self, req: Request):
        pass

    async def on_websocket(self, req: Request, ws: WebSocket) -> None:
        parsed_url = urllib.parse.urlparse(req.url)

        transport = urllib.parse.parse_qs(parsed_url.query).get('transport', ['msgpack'])[0]

        if transport not in ('msgpack'):
            return ws.close(5000)

        version = urllib.parse.parse_qs(parsed_url.query).get('v', ['1'])[0]

        if version not in ('1'):
            return ws.close(5000)

        await ws.accept()
        session = Session(ws)
        await session.start()
