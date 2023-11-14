"""Common constants for JSON encoding"""

from typing import Literal
from typing_extensions import ClassVar

from ..mapped_enum import MappedEnum


class EncoderConstants(bytes, MappedEnum):
    ## defined after effective constants in yajl and in Python json.encoder

    __finalize__: ClassVar[Literal[True]] = True

    @property
    def str_value(self) -> str:
        """string typed accessor member values"""
        if hasattr(self, "_str_value"):
            return self._str_value
        else:
            str = self.value.decode()
            self._str_value = str
            return str

    ## typed events in yajl
    # BOOLEAN = "boolean"
    # INTEGER = "integer"
    # DOUBLE = "double"
    # NUMBER = "number"
    # STRING = "string"
    ## Python json.encoder
    KEY_SEPARATOR = b":"
    ITEM_SEPARATOR = b","
    ## yajl
    START_MAP = b"{"
    MAP_KEY = b":"
    END_MAP = b"}"
    START_ARRAY = b"["
    END_ARRAY = b"]"
    ## from python json.encoder
    NULL = b"null"
    TRUE = b"true"
    FALSE = b"false"
    INFINITY = b"Infinity"
    NEGATIVE_INFINITY = b"-Infinity"
    NAN = b"NaN"

    DQUOTE = b'"'
    DQUOTE_KEY_SEPARATOR = DQUOTE + KEY_SEPARATOR

    def __eq__(self, value):
        if isinstance(value, bytes):
            return self.value == value
        elif isinstance(value, str):
            return str(self) == value
        else:
            return object.__eq__(self, value)

    def __bytes__(self):
        return self.value

    def __str__(self):
        return self.str_value

    def __hash__(self):
        return hash(self.value)

__all__ = ("EncoderConstants",)
