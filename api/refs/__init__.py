"""
api.models
~~~~~~~~~~
An API for references of objects such as messages, roles, etc.

Usage:

```py
async def route(msg_ref: MsgRef = Annotated[MsgRef, get_msg_ref]) -> None:
    message = await msg_ref.get_message()
```
"""
