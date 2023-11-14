"""Sequence-like protocol classes"""

from abc import abstractmethod
from typing import Iterable, Protocol, Union, runtime_checkable
from typing_extensions import TypeAlias, TypeVar


T_co = TypeVar("T_co", covariant=True)

StdSequenceLike: TypeAlias = Union[list, tuple, set]
"""Type alias for indexed and non-indexed sequence-like types in stdlib"""


@runtime_checkable
class SequenceLike(Iterable[T_co], Protocol):
    """Protocol class for iterable sequence-like types providing a `__len__` implementation"""
    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError(self.__len__)


@runtime_checkable
class IndexedSequenceLike(SequenceLike, Protocol):
    """Protocol class for SequenceLike types providing a `__getitem__` implementation"""
    @abstractmethod
    def __getitem__(self, key) -> T_co:
        raise NotImplementedError(self.__getitem__)


__all__ = "StdSequenceLike",  "SequenceLike", "IndexedSequenceLike"
