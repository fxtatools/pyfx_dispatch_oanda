"""GuaranteedStopLossOrderReason definition for OANDA v20 REST API, supplemental to 3.0.25"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class GuaranteedStopLossOrderReason(ApiEnum):
    """The reason that the Guaranteed Stop Loss Order was initiated
    """


    __finalize__: ClassVar[Literal[True]] = True

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
