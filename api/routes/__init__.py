"""
api.routes
~~~~~~~~~~
Route implementations for the Derailed API.

"""

from .guild import route_guilds
from .user import route_users

__all__ = ("route_users", "route_guilds")
