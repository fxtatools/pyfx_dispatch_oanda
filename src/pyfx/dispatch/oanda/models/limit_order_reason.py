
"""LimitOrderReason definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class LimitOrderReason(str, Enum):
    """
    The reason that the Limit Order was initiated
    """

    CLIENT_ORDER = 'CLIENT_ORDER'
    REPLACEMENT = 'REPLACEMENT'


__all__ = ("LimitOrderReason",)
