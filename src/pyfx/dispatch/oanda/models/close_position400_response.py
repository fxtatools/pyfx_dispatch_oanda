
"""ClosePosition400Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport import TransportField

from .response_mixins import TransactionErrorResponse
from .market_order_reject_transaction import MarketOrderRejectTransaction


class ClosePosition400Response(TransactionErrorResponse):
    """
    ClosePosition400Response: The Parameters provided that describe the Position closeout are invalid.
    """

    long_order_reject_transaction: Annotated[Optional[MarketOrderRejectTransaction], TransportField(None, alias="longOrderRejectTransaction")]
    """
    The Transaction created that rejects the creation of a MarketOrder to close the long Position.
    """

    short_order_reject_transaction: Annotated[Optional[MarketOrderRejectTransaction], TransportField(None, alias="shortOrderRejectTransaction")]
    """
    The Transaction created that rejects the creation of a MarketOrder to close the short Position.
    """


__all__ = ("ClosePosition400Response",)
