"""SetTradeClientExtensions400Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField
from .response_mixins import TransactionErrorResponse
from .trade_client_extensions_modify_reject_transaction import TradeClientExtensionsModifyRejectTransaction


class SetTradeClientExtensions400Response(TransactionErrorResponse):
    """
    SetTradeClientExtensions400Response
    """

    trade_client_extensions_modify_reject_transaction: Annotated[
        Optional[TradeClientExtensionsModifyRejectTransaction],
        TransportField(None, alias="tradeClientExtensionsModifyRejectTransaction")
        ]
    """The Transaction that rejects the modification of the Trade's Client Extensions.
    """


__all__ = ("SetTradeClientExtensions400Response",)
