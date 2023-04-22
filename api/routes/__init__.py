"""
api.routes
~~~~~~~~~~
Route implementations for the Derailed API.

"""

from .guild import route_guilds
from .invite import route_invites
from .role import route_roles
from .user import route_users

__all__ = ("route_users", "route_guilds", "route_roles", "route_invites")
