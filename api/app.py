# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from .errors import DerailedException
from .metadata import meta

derailed = FastAPI(
    title="Derailed API",
    description="OpenAPI documentation of the Derailed API",
    version="1.0.0(ALPHA): Crestella",
    default_response_class=ORJSONResponse,
)


# NOTE: streams globally prior to async setup

load_dotenv()


@derailed.on_event("startup")
async def on_startup() -> None:
    await meta.initialize()


@derailed.exception_handler(DerailedException)
def on_derailed_exception(request: Request, exc: DerailedException):
    return ORJSONResponse({"detail": exc.inspect()}, status_code=exc.code)
