# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from typing import Annotated

from fastapi import APIRouter
from pydantic import Field

from api.refs import current_guild

from ..errors import CustomError
from ..flags import DEFAULT_PERMISSIONS, RolePermissions
from ..models.role import Role
from ..refs.current_guild import CurrentGuildRef
from ..utils import MISSING, Maybe

role_routes = APIRouter()


class CreateRole:
    name: str
    allow: Maybe[int] = Field(MISSING)
    deny: Maybe[int] = Field(MISSING)
    position: Maybe[int] = Field(MISSING)


class ModifyRole:
    name: Maybe[str] = Field(MISSING)
    allow: Maybe[int] = Field(MISSING)
    deny: Maybe[int] = Field(MISSING)
    position: Maybe[int] = Field(MISSING)


@role_routes.post("/guilds/{guild_id}/roles")
async def create_role(
    guild_ref: Annotated[CurrentGuildRef, current_guild], payload: CreateRole
):
    member = await guild_ref.get_member(
        RolePermissions.MANAGE_ROLES, guild=await guild_ref.get_guild()
    )

    highest_role_position = await member.highest_role_position()

    if payload.position and payload.position >= highest_role_position:
        raise CustomError("Requested position is higher than current")

    role = await Role.create(
        name=payload.name,
        guild_id=guild_ref.guild_id,
        allow=payload.allow or DEFAULT_PERMISSIONS.value,
        deny=payload.deny or 0,
        position=payload.position,
    )

    return await role.publicize()


@role_routes.get("/guilds/{guild_id}/roles")
async def get_guild_roles(guild_ref: Annotated[CurrentGuildRef, current_guild]):
    await guild_ref.get_member()

    roles = await Role.acquire_all(guild_ref.guild_id)

    return [await role.publicize() for role in roles]


@role_routes.get("/guilds/{guild_id}/roles/{role_id}")
async def get_guild_role(
    guild_ref: Annotated[CurrentGuildRef, current_guild], role_id: int
):
    await guild_ref.get_member()

    role = await Role.acquire(role_id)

    return await role.publicize()


@role_routes.patch("/guilds/{guild_id}/roles/{role_id}")
async def modify_guild_role(
    guild_ref: Annotated[CurrentGuildRef, current_guild],
    role_id: int,
    payload: ModifyRole,
):
    member = await guild_ref.get_member(
        RolePermissions.MANAGE_ROLES, guild=await guild_ref.get_guild()
    )

    highest_role_position = await member.highest_role_position()

    role = await Role.acquire(role_id)

    if role.position >= highest_role_position:
        raise CustomError(
            "This role is too high to be modified with current permissions"
        )

    if payload.name:
        role.name = payload.name

    if payload.allow:
        role.allow = RolePermissions(payload.allow)

    if payload.deny:
        role.deny = RolePermissions(payload.deny)

    await role.modify()

    return await role.publicize()


@role_routes.delete("/guilds/{guild_id}/roles/{role_id}")
async def delete_guild_role(
    guild_ref: Annotated[CurrentGuildRef, current_guild], role_id: int
):
    member = await guild_ref.get_member(
        RolePermissions.MANAGE_ROLES, guild=await guild_ref.get_guild()
    )

    highest_role_position = await member.highest_role_position()

    role = await Role.acquire(role_id)

    if role.position >= highest_role_position:
        raise CustomError("Cannot delete role above your own")

    await role.delete()

    return ""
