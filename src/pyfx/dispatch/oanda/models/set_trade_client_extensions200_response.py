"""SetTradeClientExtensions200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField
from .response_mixins import TransactionResponse
from .trade_client_extensions_modify_transaction import TradeClientExtensionsModifyTransaction


class SetTradeClientExtensions200Response(TransactionResponse):
    """
    SetTradeClientExtensions200Response
    """

    trade_client_extensions_modify_transaction: Annotated[
        Optional[TradeClientExtensionsModifyTransaction],
        TransportField(None, alias="tradeClientExtensionsModifyTransaction")
    ]
    """The Transaction that updates the Trade's Client Extensions.
    """


__all__ = ("SetTradeClientExtensions200Response",)
