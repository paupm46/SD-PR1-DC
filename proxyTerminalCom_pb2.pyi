from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Coefficients(_message.Message):
    __slots__ = ["pollution_mean", "timestamp", "wellness_mean"]
    POLLUTION_MEAN_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    WELLNESS_MEAN_FIELD_NUMBER: _ClassVar[int]
    pollution_mean: float
    timestamp: _timestamp_pb2.Timestamp
    wellness_mean: float
    def __init__(self, wellness_mean: _Optional[float] = ..., pollution_mean: _Optional[float] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
