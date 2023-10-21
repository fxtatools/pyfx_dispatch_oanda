"""GuaranteedStopLossOrderReason definition for OANDA v20 REST API, supplemental to 3.0.25"""

from enum import Enum


class GuaranteedStopLossOrderReason(str, Enum):
    """The reason that the Guaranteed Stop Loss Order was initiated
    """

    CLIENT_ORDER = "CLIENT_ORDER"
    """The Guaranteed Stop Loss Order was initiated at the request of a client
    """

    REPLACEMENT = "REPLACEMENT"
    """The Guaranteed Stop Loss Order was initiated as a replacement for an existing Order
    """

    ON_FILL =  "ON_FILL"
    """The Guaranteed Stop Loss Order was initiated automatically when an Order was filled
    that opened a new Trade requiring a Guaranteed Stop Loss Order.
    """

__all__ = ("GuaranteedStopLossOrderReason",)
