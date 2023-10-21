"""TradePL definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class TradePL(str, Enum):
    """
    The classification of TradePLs.
    """

    POSITIVE = 'POSITIVE'
    NEGATIVE = 'NEGATIVE'
    ZERO = 'ZERO'


__all__ = ("TradePL",)
