"""Common definitions for transport protocol support"""

from ..mapped_enum import MappedEnum
from collections.abc import Mapping
from typing import Any
from typing_extensions import TypeAlias

IntermediateObject: TypeAlias = Mapping[str, Any]
"""Type alias for intermediate representations of JSON objects"""


class RequestConstants(str, MappedEnum):
    NULL = "null"
    TRUE = "true"
    FALSE = "false"

class RequestByteConstants(bytes, MappedEnum):
    NULL = b"null"
    TRUE = b"true"
    FALSE = b"false"


__all__ = "IntermediateObject", "RequestConstants", "RequestByteConstants"
