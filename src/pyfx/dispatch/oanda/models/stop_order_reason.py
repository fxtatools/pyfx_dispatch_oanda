
"""StopOrderReason definition for OANDA v20 REST API (3.0.25)"""


from enum import Enum


class StopOrderReason(str, Enum):
    """
    The reason that the Stop Order was initiated
    """

    CLIENT_ORDER = 'CLIENT_ORDER'
    REPLACEMENT = 'REPLACEMENT'


__all__ = ("StopOrderReason",)
