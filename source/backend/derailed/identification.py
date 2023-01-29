"""
Copyright (C) 2021-2023 Derailed.

Under no circumstances may you publicly share, distribute, or give any objects, files, or media in this project.
You may only share the above with individuals who have permission to view these files already.
If they don't have permission but are still given the files, or if code is shared publicly, 
we have the legal jurisdiction to bring forth charges under which is owed, based in the damages.

You may under some circumstances with authorized permission share snippets of the code for specific reasons.
Any media and product here must be kept proprietary unless otherwise necessary or authorized.
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
