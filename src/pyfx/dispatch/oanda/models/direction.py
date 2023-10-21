"""Direction definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class Direction(str, Enum):
    """
    In the context of an Order or a Trade, defines whether the units are positive or negative.
    """

    LONG = 'LONG'
    SHORT = 'SHORT'


__all__ = ("Direction",)
