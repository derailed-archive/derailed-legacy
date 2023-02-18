"""
Copyright (C) 2021-2023 Derailed

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import secrets
import threading
import time
from random import randint
from typing import Callable

from fastapi import APIRouter

versions = 1
default_version = 1


class IDMedium:
    def __init__(self, epoch: int = 1672531200000) -> None:
        self._incr: int = 0
        self._epoch = epoch

    def snowflake(self) -> int:
        current_ms = int(time.time() * 1000)
        epoch = current_ms - self._epoch << 22

        curthread = threading.current_thread().ident
        if curthread is None:
            raise AssertionError

        epoch |= (curthread % 32) << 17
        epoch |= (os.getpid() % 32) << 12

        epoch |= self._incr % 4096

        if self._incr == 9000000000:
            self._incr = 0

        self._incr += 1

        return epoch

    def invite(self) -> str:
        return secrets.token_urlsafe(randint(4, 9))


medium = IDMedium()


def version(
    path: str,
    minimum_version: int,
    router: APIRouter,
    method: str,
    exclude_versions_higher: int = 0,
    **kwargs,
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        for version in range(versions):
            version += 1

            if not version <= minimum_version:
                continue
            elif version > versions:
                break
            elif exclude_versions_higher > version:
                break

            router.add_api_route(
                f'/v{minimum_version}{path}', func, methods=[method], **kwargs
            )

            if minimum_version == default_version:
                router.add_api_route(f'/{path}', func, methods=[method], **kwargs)
        return func

    return wrapper
