# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


class DerailedException(Exception):
    def inspect(self) -> str:
        return "No error details"


class InternalException(DerailedException):
    def inspect(self) -> str:
        return "Internal Server Exception"


class UserDoesNotExist(DerailedException):
    def inspect(self) -> str:
        return "Specified user does not exist in some form"


class UsernameOverused(DerailedException):
    def inspect(self) -> str:
        return "Username is overused, try another one"
