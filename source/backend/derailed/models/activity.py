"""
Copyright (C) 2021-2023 Derailed.

Under no circumstances may you publicly share, distribute, or give any objects, files, or media in this project.
You may only share the above with individuals who have permission to view these files already.
If they don't have permission but are still given the files, or if code is shared publicly, 
we have the legal jurisdiction to bring forth charges under which is owed, based in the damages.

You may under some circumstances with authorized permission share snippets of the code for specific reasons.
Any media and product here must be kept proprietary unless otherwise necessary or authorized.
"""
from datetime import datetime
from enum import Enum

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ActivityType(Enum):
    CUSTOM = 0


class Activity(Base):
    __tablename__ = 'activities'

    user_id: Mapped[int] = mapped_column(
        BigInteger(), ForeignKey('users.id'), primary_key=True
    )
    type: Mapped[ActivityType]
    created_at: Mapped[datetime]
    content: Mapped[str] = mapped_column(String(15))
