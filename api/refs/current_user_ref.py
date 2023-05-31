# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from typing import Annotated

from fastapi import Header

from ..errors import CustomError, InvalidToken, UserDoesNotExist
from ..identity import get_token_user_id, verify_token
from ..models.user import User
from .base import Ref


class CurUserRef(Ref):
    def __init__(self, token: str) -> None:
        self.__token = token

    @property
    def user_id(self) -> int:
        """Parse the token of this ref and return the user id given."""

        return get_token_user_id(self.__token)

    async def get_user(self) -> User:
        """Verifies user identity then returns user.
        Raises an error if identity is invalid.
        """

        user_id = self.user_id

        try:
            user = await User.acquire(user_id)
        except UserDoesNotExist:
            raise InvalidToken

        verify_token(user, self.__token)

        return user


def cur_ref(token: Annotated[str, Header(alias="authorization")]) -> CurUserRef:
    return CurUserRef(token=token)


async def admin(ref: Annotated[CurUserRef, cur_ref]) -> User:
    user = await ref.get_user()

    if not user.flags.staff:
        raise CustomError("Path forbidden", 403)

    return user
