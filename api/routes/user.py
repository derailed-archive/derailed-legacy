# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from typing import Annotated

import bcrypt
import pydantic
from fastapi import APIRouter

from ..errors import CustomError
from ..metadata import meta
from ..models.user import User
from ..refs.current_user_ref import CurUserRef, cur_ref
from ..utils import MISSING, Missing

route_users = APIRouter()


class RegisterData(pydantic.BaseModel):
    username: str = pydantic.Field(max_length=32, min_length=2)
    password: str = pydantic.Field(max_length=72, min_length=2)
    email: str = pydantic.Field(max_length=100, min_length=5)


class ModifySelfData(pydantic.BaseConfig):
    password: str | Missing = pydantic.Field(MISSING, max_length=72, min_length=2)
    old_password: str = pydantic.Field(max_length=72, min_length=2)
    email: pydantic.EmailStr | Missing = pydantic.Field(
        MISSING, max_length=100, min_length=5
    )


class DeleteSelfData(pydantic.BaseConfig):
    password: str | Missing = pydantic.Field(MISSING, max_length=72, min_length=2)


@route_users.post("/register")
async def register(payload: RegisterData):
    """Registers a new user to Derailed."""

    salt = bcrypt.gensalt(14)
    password = bcrypt.hashpw(payload.password.encode(), salt)

    user = await User.register(
        meta.genflake(), payload.username, payload.email, password.decode()
    )

    return await user.publicize(secure=True)


@route_users.patch("/users/@me")
async def modify_current_user(
    ref: Annotated[CurUserRef, cur_ref], payload: ModifySelfData
):
    """Modifies the current user."""

    user = await ref.get_user()

    if bcrypt.checkpw(payload.old_password.encode(), user.password.encode()) is False:
        raise CustomError("Invalid password")

    if payload.password is not MISSING:
        salt = bcrypt.gensalt(14)
        password = bcrypt.hashpw(payload.password.encode(), salt)
        user.password = password.decode()

    if payload.email is not MISSING:
        user.email = str(payload.email)

    await user.modify()

    return await user.publicize(secure=True)


@route_users.get("/users/@me")
async def get_current_user(ref: Annotated[CurUserRef, cur_ref]):
    """Route for fetching the current user of this token."""

    return await (await ref.get_user()).publicize(secure=True)


@route_users.delete("/users/@me")
async def delete_current_user(
    ref: Annotated[CurUserRef, cur_ref], payload: DeleteSelfData
):
    """Deletes the current user immediately."""

    user = await ref.get_user()
    await user.delete()

    return ""
