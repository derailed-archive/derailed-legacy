# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed

import base64
import binascii

import itsdangerous

from .errors import InvalidToken
from .models.user import User


def create_token(user: User) -> str:
    user_id = base64.urlsafe_b64encode(str(user.id).encode())

    signer = itsdangerous.TimestampSigner(user.password)
    return signer.sign(user_id).decode()


def get_token_user_id(token: str) -> str:
    fragmented = token.split(".")
    encoded_id = fragmented[0]

    return int(base64.b64decode(encoded_id.encode()).decode())


def verify_token(user: User, token: str) -> None:
    try:
        get_token_user_id(token)
    # try to prevent every error and spin it back to the user
    except (IndexError, binascii.Error, UnicodeDecodeError, ValueError):
        raise InvalidToken

    signer = itsdangerous.TimestampSigner(user.password)

    try:
        signer.unsign(token)
    except itsdangerous.BadSignature:
        raise InvalidToken
