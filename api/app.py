# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

from typing import Any, Callable

import msgspec
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from .errors import DerailedException
from .metadata import meta
from .routes import route_guilds, route_invites, route_roles, route_users


class MSGSpecResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return msgspec.json.encode(content)


class MSGSpecRequest(Request):
    async def json(self) -> Any:
        if not hasattr(self, "_json"):
            body = await self.body()
            self._json = msgspec.json.decode(body)
        return self._json


class MSGSpecRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = MSGSpecRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


derailed = FastAPI(
    title="Derailed API",
    description="OpenAPI documentation of the Derailed API",
    version="1.0.0(ALPHA): Crestella",
    default_response_class=MSGSpecResponse,
)
derailed.router.route_class = MSGSpecRoute

derailed.include_router(route_users)
derailed.include_router(route_guilds)
derailed.include_router(route_roles)
derailed.include_router(route_invites)


# NOTE: streams globally prior to async setup

load_dotenv()


@derailed.on_event("startup")
async def on_startup() -> None:
    await meta.initialize()


@derailed.exception_handler(DerailedException)
def on_derailed_exception(request: Request, exc: DerailedException):
    return MSGSpecResponse({"detail": exc.inspect()}, status_code=exc.code)
