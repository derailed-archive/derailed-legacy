# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

from dotenv import load_dotenv
from fastapi import FastAPI

from .metadata import meta

derailed = FastAPI(
    title="Derailed API",
    description="OpenAPI documentation of the Derailed API",
    version="1.0.0(ALPHA): Crestella",
)


# NOTE: streams globally prior to async setup

load_dotenv()


@derailed.on_event("startup")
async def on_startup() -> None:
    await meta.initialize()
