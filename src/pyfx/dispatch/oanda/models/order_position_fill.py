
"""OrderPositionFill definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class OrderPositionFill(str, Enum):
    """
    Specification of how Positions in the Account are modified when the Order is filled.
    """

    OPEN_ONLY = 'OPEN_ONLY'
    REDUCE_FIRST = 'REDUCE_FIRST'
    REDUCE_ONLY = 'REDUCE_ONLY'
    DEFAULT = 'DEFAULT'


__all__ = ("OrderPositionFill",)
