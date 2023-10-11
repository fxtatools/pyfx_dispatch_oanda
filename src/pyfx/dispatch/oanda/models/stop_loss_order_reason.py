
"""StopLossOrderReason definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class StopLossOrderReason(str, Enum):
    """
    The reason that the Stop Loss Order was initiated
    """

    CLIENT_ORDER = 'CLIENT_ORDER'
    REPLACEMENT = 'REPLACEMENT'
    ON_FILL = 'ON_FILL'


__all__ = ("StopLossOrderReason",)
