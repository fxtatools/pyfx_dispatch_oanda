
"""TrailingStopLossOrderReason definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class TrailingStopLossOrderReason(str, Enum):
    """
    The reason that the Trailing Stop Loss Order was initiated
    """

    CLIENT_ORDER = 'CLIENT_ORDER'
    REPLACEMENT = 'REPLACEMENT'
    ON_FILL = 'ON_FILL'


__all__ = ("TrailingStopLossOrderReason",)
