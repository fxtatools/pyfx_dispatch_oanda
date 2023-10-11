
"""ClosePosition404Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport import TransportField

from .response_mixins import TransactionErrorResponse
from .market_order_reject_transaction import MarketOrderRejectTransaction


class ClosePosition404Response(TransactionErrorResponse):
    """
    ClosePosition404Response: The Account or one or more of the Positions specified does not exist.
    """

    long_order_reject_transaction: Optional[MarketOrderRejectTransaction] = TransportField(None, alias="longOrderRejectTransaction")
    """
    The Transaction created that rejects the creation of a MarketOrder to close the long Position. Only present if the Account exists and a long Position was specified.
    """

    short_order_reject_transaction: Optional[MarketOrderRejectTransaction] = TransportField(None, alias="shortOrderRejectTransaction")
    """
    The Transaction created that rejects the creation of a MarketOrder to close the short Position. Only present if the Account exists and a short Position was specified.
    """


__all__ = ("ClosePosition404Response",)
