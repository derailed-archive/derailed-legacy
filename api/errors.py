# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


class DerailedException(Exception):
    code: int = 500

    def inspect(self) -> str:
        return "No error details"


class InternalException(DerailedException):
    def inspect(self) -> str:
        return "Internal Server Exception"


class UserDoesNotExist(DerailedException):
    code = 404

    def inspect(self) -> str:
        return "Specified user does not exist in some form"


class GuildDoesNotExist(DerailedException):
    code = 404

    def inspect(self) -> str:
        return "Specified guild does not exist in some form"


class UsernameOverused(DerailedException):
    code = 400

    def inspect(self) -> str:
        return "Username is overused, try another one"


class InvalidToken(DerailedException):
    code = 401

    def inspect(self) -> str:
        return "Token given is invalid"


class CustomError(DerailedException):
    def __init__(self, msg: str, code: int = 400) -> None:
        super().__init__(msg, code)
        self.code = code
        self.msg = msg

    def inspect(self) -> str:
        return self.msg
