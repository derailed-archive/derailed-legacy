# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from functools import cached_property, lru_cache
from typing import Annotated, NotRequired, TypedDict

import jwt
from fastapi import Header

from ..errors import InvalidToken
from ..models.user import User
from .base import Ref


class JWTFormat(TypedDict):
    session_id: NotRequired[str]
    bot: NotRequired[bool]


class CurUserRef(Ref):
    def __init__(self, token: str) -> None:
        self.__token = token

    @cached_property
    def user_id(self) -> int:
        """Parse the token of this ref and return the user id given."""

        try:
            header = jwt.get_unverified_header(self.__token)
        except jwt.InvalidTokenError:
            raise InvalidToken

        try:
            return int(header["jti"])
        except (KeyError, ValueError):
            raise InvalidToken

    @lru_cache
    async def get_user(self) -> User:
        """Verifies user identity then returns user.
        Raises an error if identity is invalid.

        **This is an async property, and henceforth must be awaited to be used.**
        """

        user_id = self.user_id

        user = await User.acquire(user_id)

        try:
            decoded_jwt: JWTFormat = jwt.decode(self.__token, user.password, ["HS512"])
        except jwt.InvalidTokenError:
            raise InvalidToken

        session_id = decoded_jwt.get("session_id")
        bot = decoded_jwt.get("bot")

        if session_id is None or bot is None:
            raise InvalidToken

        # to save space, bots don't register sessions.
        if bot:
            return user

        # TODO: verify sessions

        return user


def cur_ref(token: Annotated[str, Header(alias="authorization")]) -> CurUserRef:
    return CurUserRef(token=token)
