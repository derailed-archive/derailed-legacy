# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from typing import Annotated, Literal

import bcrypt
import pydantic
from fastapi import APIRouter, Depends

from ..errors import CustomError
from ..identity import create_token
from ..metadata import meta
from ..models.user import User
from ..refs.current_user_ref import CurUserRef, cur_ref
from ..utils import MISSING, Maybe

route_users = APIRouter()


class RegisterData(pydantic.BaseModel):
    username: str = pydantic.Field(max_length=32, min_length=2)
    password: str = pydantic.Field(max_length=72, min_length=2)
    email: str = pydantic.Field(max_length=100, min_length=5)


class ModifySelfData(pydantic.BaseModel):
    password: Maybe[str] = pydantic.Field(MISSING, max_length=72, min_length=2)
    old_password: str = pydantic.Field(max_length=72, min_length=2)
    email: Maybe[pydantic.EmailStr] = pydantic.Field(MISSING)


class DeleteSelfData(pydantic.BaseModel):
    password: Maybe[str] = pydantic.Field(MISSING, max_length=72, min_length=2)


class ModifySettings(pydantic.BaseModel):
    theme: Maybe[Literal["dark", "light"]] = pydantic.Field(MISSING)
    status: Maybe[Literal[0, 1, 2, 3]] = pydantic.Field(MISSING)


@route_users.post("/register")
async def register(payload: RegisterData):
    """Registers a new user to Derailed."""

    if len(payload.email) > 100:
        raise CustomError("Email must be under 100 characters")
    elif len(payload.email) < 5:
        raise CustomError("Email must be over 5 characters")

    salt = bcrypt.gensalt(14)
    password = bcrypt.hashpw(payload.password.encode(), salt)

    user = await User.register(
        meta.genflake(), payload.username, payload.email, password.decode()
    )

    pub = await user.publicize(secure=True)
    pub["token"] = create_token(user)
    return pub


@route_users.patch("/users/@me")
async def modify_current_user(
    payload: ModifySelfData, ref: Annotated[CurUserRef, Depends(cur_ref)]
):
    """Modifies the current user."""

    user = await ref.get_user()

    if bcrypt.checkpw(payload.old_password.encode(), user.password.encode()) is False:
        raise CustomError("Invalid password")

    if payload.email:
        if len(payload.email) > 100:
            raise CustomError("Email must be under 100 characters")
        elif len(payload.email) < 5:
            raise CustomError("Email must be over 5 characters")

        user.email = str(payload.email)

    if payload.password:
        salt = bcrypt.gensalt(14)
        password = bcrypt.hashpw(payload.password.encode(), salt)
        user.password = password.decode()

    await user.modify()

    return await user.publicize(secure=True)


@route_users.get("/users/@me")
async def get_current_user(ref: Annotated[CurUserRef, Depends(cur_ref)]):
    """Route for fetching the current user of this token."""

    return await (await ref.get_user()).publicize(secure=True)


@route_users.get("/users/@me/settings")
async def get_settings(ref: Annotated[CurUserRef, Depends(cur_ref)]):
    """Get the settings of the current user."""

    user = await ref.get_user()
    settings = await user.get_settings()

    return await settings.publicize()


@route_users.patch("/users/@me/settings")
async def modify_settings(
    ref: Annotated[CurUserRef, Depends(cur_ref)], pd: ModifySettings
):
    """Modify this users' settings."""

    user = await ref.get_user()

    settings = await user.get_settings()

    if pd != {}:
        if pd.theme:
            settings.theme = pd.theme

        if pd.status is not MISSING:
            settings.status = pd.status

        await settings.modify()

    return await settings.publicize()


@route_users.delete("/users/@me")
async def delete_current_user(
    payload: DeleteSelfData, ref: Annotated[CurUserRef, Depends(cur_ref)]
):
    """Deletes the current user immediately."""

    user = await ref.get_user()
    await user.delete()

    return ""
