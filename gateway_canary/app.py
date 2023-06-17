# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


import urllib.parse

from falcon.asgi import App, Request, WebSocket

from .session import Session


class WebSocketResource:
    async def on_get(self, req: Request):
        pass

    async def on_websocket(self, req: Request, ws: WebSocket) -> None:
        parsed_url = urllib.parse.urlparse(req.url)
        pql = urllib.parse.parse_qs(parsed_url.query)

        transport = pql.get("transport", ["msgpack"])[0]

        if transport not in ("msgpack"):
            return ws.close(5000)

        version = pql.get("v", ["1"])[0]

        if version not in ("1"):
            return ws.close(5000)

        await ws.accept()
        session = Session(ws, version, transport)
        await session.start()


# run python -m socketify gateway_canary.app:app --ws gateway_canary.app:ws --port 9090
ws = app = App()
app.add_route("/", WebSocketResource())
