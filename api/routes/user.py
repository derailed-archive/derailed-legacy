# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from typing import Annotated

import bcrypt
import pydantic
from fastapi import APIRouter

from ..metadata import meta
from ..models.user import User
from ..refs.current_user_ref import CurUserRef, cur_ref

route_users = APIRouter()


class RegisterData(pydantic.BaseModel):
    username: str = pydantic.Field(max_length=32, min_length=2)
    password: str = pydantic.Field(max_length=72, min_length=2)
    email: str = pydantic.Field(max_length=100, min_length=5)


@route_users.post("/register")
async def register(payload: RegisterData):
    """Registers a new user to Derailed."""

    salt = bcrypt.gensalt(14)
    password = bcrypt.hashpw(payload.password.encode(), salt)

    user = await User.register(
        meta.genflake(), payload.username, payload.email, password.decode()
    )

    return await user.publicize(secure=True)


@route_users.get("/users/@me")
async def get_current_user(ref: Annotated[CurUserRef, cur_ref]):
    """Route for fetching the current user of this token."""

    return await (await ref.get_user()).publicize(secure=True)
