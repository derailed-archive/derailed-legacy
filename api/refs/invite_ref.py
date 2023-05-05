# SPDX-License-Identifier: AGPL-3.0
# Part of the Derailed Project
# Copyright 2021-2023 Derailed


from typing import Annotated

from fastapi import Path

from ..models.invites import Invite


class InviteRef:
    def __init__(self, invite_id: str) -> None:
        self.id = invite_id

    async def get(self) -> Invite:
        return await Invite.acquire(self.id)


def invite_ref(invite_id: Annotated[str, Path()]) -> InviteRef:
    return InviteRef(invite_id)
