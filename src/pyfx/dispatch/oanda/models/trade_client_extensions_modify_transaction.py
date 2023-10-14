
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional

from .client_extensions import ClientExtensions

from ..transport.transport_fields import TransportField
from ..util import exporting

from .transaction import Transaction
from .transaction_type import TransactionType
from .common_types import TradeId, ClientId


class TradeClientExtensionsModifyTransaction(Transaction):
    """
    A TradeClientExtensionsModifyTransaction represents the modification of a Trade's Client Extensions.
    """

    type: Annotated[Literal[TransactionType.TRADE_CLIENT_EXTENSIONS_MODIFY], TransportField(TransactionType.TRADE_CLIENT_EXTENSIONS_MODIFY)] = TransactionType.TRADE_CLIENT_EXTENSIONS_MODIFY
    """
    The Type of the Transaction. Always set to \"TRADE_CLIENT_EXTENSIONS_MODIFY\" for a TradeClientExtensionsModifyTransaction.
    """

    trade_id: Annotated[Optional[TradeId], TransportField(None, alias="tradeID")]
    """
    The ID of the Trade who's client extensions are to be modified.
    """

    client_trade_id: Annotated[Optional[ClientId], TransportField(None, alias="clientTradeID")]
    """
    The original Client ID of the Trade who's client extensions are to be modified.
    """

    trade_client_extensions_modify: Annotated[Optional[ClientExtensions], TransportField(None, alias="tradeClientExtensionsModify")]


__all__ = exporting(__name__, ...)
