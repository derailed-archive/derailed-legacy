from typing import ClassVar as _ClassVar
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class GetGuildInfo(_message.Message):
    __slots__ = ['guild_id']
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: str
    def __init__(self, guild_id: _Optional[str] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ['data', 'event']
    DATA_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    data: str
    event: str
    def __init__(self, event: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...

class Publ(_message.Message):
    __slots__ = ['guild_id', 'message']
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    guild_id: str
    message: Message
    def __init__(
        self, guild_id: _Optional[str] = ..., message: _Optional[_Union[Message, _Mapping]] = ...
    ) -> None: ...

class Publr(_message.Message):
    __slots__ = ['message']
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class RepliedGuildInfo(_message.Message):
    __slots__ = ['available', 'presences']
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    PRESENCES_FIELD_NUMBER: _ClassVar[int]
    available: bool
    presences: int
    def __init__(self, presences: _Optional[int] = ..., available: bool = ...) -> None: ...

class UPubl(_message.Message):
    __slots__ = ['message', 'user_id']
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    message: Message
    user_id: str
    def __init__(
        self, user_id: _Optional[str] = ..., message: _Optional[_Union[Message, _Mapping]] = ...
    ) -> None: ...

class UPublr(_message.Message):
    __slots__ = ['message']
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
