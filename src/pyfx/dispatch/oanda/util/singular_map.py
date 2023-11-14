"""SingularMap class definition"""

from collections.abc import Mapping
from typing import Iterator, Literal
from typing_extensions import TypeVar

T_key = TypeVar("T_key")
T_val = TypeVar("T_val")


class SingularMap(Mapping[T_key, T_val]):
    """Mapping representation of a single key, value pair"""

    __slots__ = "key", "value"
    key: T_key
    value: T_val

    def __init__(self, key: T_key, value: T_val):
        self.key = key
        self.value = value

    def keys(self) -> Iterator[T_key]:
        yield self.key

    def values(self) -> Iterator[T_val]:
        yield self.value

    def items(self) -> Iterator[tuple[T_key, T_val]]:
        yield self.key, self.value

    def __getitem__(self, key: T_key) -> T_val:
        if key is self.key:
            return self.value
        else:
            raise KeyError("Unknown key", key)

    def __iter__(self) -> Iterator[T_key]:
        yield self.key

    def __len__(self) -> Literal[1]:
        return 1

    def __repr__(self) -> str:
        return "<%s %s: %r at 0x%x>" % (self.__class__.__name__, self.key, self.value, id(self),)


__all__ = ("SingularMap",)
