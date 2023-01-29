"""
Copyright (C) 2021-2023 Derailed.

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
from datetime import datetime
from enum import Enum

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ActivityType(Enum):
    CUSTOM = 0


class Activity(Base):
    __tablename__ = 'activities'

    user_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('users.id'), primary_key=True)
    type: Mapped[ActivityType]
    created_at: Mapped[datetime]
    content: Mapped[str] = mapped_column(String(15))
