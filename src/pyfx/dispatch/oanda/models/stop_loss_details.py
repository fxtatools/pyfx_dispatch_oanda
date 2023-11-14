"""StopLossDetails model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField
from .trade_dependent_mixins import TradeDependentPriceDetails


class StopLossDetails(TradeDependentPriceDetails):
    """StopLossDetails specifies the details of a Stop Loss Order to be created on behalf of a client.

    This may happen when an Order is filled that opens a Trade requiring a Stop Loss, or when a Trade's
    dependent Stop Loss Order is modified directly through the Trade.
    """

    guaranteed: Annotated[Optional[bool], TransportField(None, deprecated=True)]
    """Flag indicating that the price for the Stop Loss Order is guaranteed.

    The default value depends on the GuaranteedStopLossOrderMode of the account.
    If it is REQUIRED, the default will be true, for DISABLED or ENABLED the default is false.
    """


__all__ = ("StopLossDetails",)
