# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auth.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\nauth.proto\x12\x12\x64\x65railed.grpc.auth"0\n\x0b\x43reateToken\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t"\x19\n\x08NewToken\x12\r\n\x05token\x18\x01 \x01(\t"A\n\rValidateToken\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\r\n\x05token\x18\x03 \x01(\t"\x16\n\x05Valid\x12\r\n\x05valid\x18\x01 \x01(\x08\x32\xa6\x01\n\rAuthorization\x12I\n\x06\x63reate\x12\x1f.derailed.grpc.auth.CreateToken\x1a\x1c.derailed.grpc.auth.NewToken"\x00\x12J\n\x08validate\x12!.derailed.grpc.auth.ValidateToken\x1a\x19.derailed.grpc.auth.Valid"\x00\x42\x34\n\x16one.derailed.grpc.authB\x11\x44\x65railedAuthProtoP\x01\xa2\x02\x04\x44RLPb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'auth_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS is False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = (
        b'\n\026one.derailed.grpc.authB\021DerailedAuthProtoP\001\242\002\004DRLP'
    )
    _CREATETOKEN._serialized_start = 34 # type: ignore
    _CREATETOKEN._serialized_end = 82 # type: ignore
    _NEWTOKEN._serialized_start = 84 # type: ignore
    _NEWTOKEN._serialized_end = 109 # type: ignore
    _VALIDATETOKEN._serialized_start = 111 # type: ignore
    _VALIDATETOKEN._serialized_end = 176 # type: ignore
    _VALID._serialized_start = 178 # type: ignore
    _VALID._serialized_end = 200 # type: ignore
    _AUTHORIZATION._serialized_start = 203 # type: ignore
    _AUTHORIZATION._serialized_end = 369 # type: ignore
# @@protoc_insertion_point(module_scope)
