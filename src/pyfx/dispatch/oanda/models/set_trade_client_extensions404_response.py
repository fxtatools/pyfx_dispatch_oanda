"""SetTradeClientExtensions404Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField
from .response_mixins import TransactionErrorResponse
from .trade_client_extensions_modify_reject_transaction import TradeClientExtensionsModifyRejectTransaction


class SetTradeClientExtensions404Response(TransactionErrorResponse):
    """
    SetTradeClientExtensions404Response
    """

    trade_client_extensions_modify_reject_transaction: Annotated[Optional[TradeClientExtensionsModifyRejectTransaction], TransportField(None, alias="tradeClientExtensionsModifyRejectTransaction")]
    """The Transaction that rejects the modification of the Trade's Client Extensions.

    Only present if the Account exists.
    """


__all__ = ("SetTradeClientExtensions404Response",)
