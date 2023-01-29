from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class CreateToken(_message.Message):
    __slots__ = ['password', 'user_id']
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    password: str
    user_id: str
    def __init__(self, user_id: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class NewToken(_message.Message):
    __slots__ = ['token']
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class Valid(_message.Message):
    __slots__ = ['valid']
    VALID_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    def __init__(self, valid: bool = ...) -> None: ...

class ValidateToken(_message.Message):
    __slots__ = ['password', 'token', 'user_id']
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    password: str
    token: str
    user_id: str
    def __init__(
        self, user_id: _Optional[str] = ..., password: _Optional[str] = ..., token: _Optional[str] = ...
    ) -> None: ...
