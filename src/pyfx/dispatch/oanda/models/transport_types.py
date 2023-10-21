"""Supplemental transport type definitions"""

from json import JSONEncoder
from numpy import double
from typing import Optional

from .common_types import DoubleConstants
from ..transport.transport_base import TransportType


class TransportDecmialAll(TransportType[float, str]):
    """Transport type interface for values encoded as "ALL" or a decimal string

    This transport type will interpret "ALL" as DoubleConstants.INF.value,
    i.e as a reusable instance of numpy 'inf'.

    A decimal string will be interpreted as a `numpy.double` value

    For `unprase()`, the parser interpretation is symmetrical.
    """

    @classmethod
    def parse(cls, value: str | float) -> float:
        if isinstance(value, float):
            return value
        elif value == "ALL":
            return DoubleConstants.INF.value  # type: ignore
        else:
            return double(value)  # type: ignore

    @classmethod
    def unparse(cls, value: float, encoder: Optional[JSONEncoder] = None) -> str:
        if value == DoubleConstants.INF:
            return "ALL"
        else:
            return str(value)

__all__ = ("TransportDecmialAll",)
