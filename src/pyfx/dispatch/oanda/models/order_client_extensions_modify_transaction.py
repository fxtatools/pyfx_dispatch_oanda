
"""OrderClientExtensionsModifyTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional

from .client_extensions import ClientExtensions

from ..transport.transport_fields import TransportField

from .transaction import Transaction
from .transaction_type import TransactionType
from .common_types import OrderId, ClientId


class OrderClientExtensionsModifyTransaction(Transaction):
    """
    A OrderClientExtensionsModifyTransaction represents the modification of an Order's Client Extensions.
    """

    type: Annotated[Literal[TransactionType.ORDER_CLIENT_EXTENSIONS_MODIFY], TransportField(TransactionType.ORDER_CLIENT_EXTENSIONS_MODIFY)] = TransactionType.ORDER_CLIENT_EXTENSIONS_MODIFY
    """
    The Type of the Transaction. Always set to \"ORDER_CLIENT_EXTENSIONS_MODIFY\" for a OrderClienteExtensionsModifyTransaction.
    """

    order_id: Annotated[Optional[OrderId], TransportField(None, alias="orderID")]
    """
    The ID of the Order who's client extensions are to be modified.
    """

    client_order_id: Annotated[Optional[ClientId], TransportField(None, alias="clientOrderID")]
    """
    The original Client ID of the Order who's client extensions are to be modified.
    """

    client_extensions_modify: Annotated[Optional[ClientExtensions], TransportField(None, alias="clientExtensionsModify")]
    
    trade_client_extensions_modify: Annotated[Optional[ClientExtensions], TransportField(None, alias="tradeClientExtensionsModify")]


__all__ = ("OrderClientExtensionsModifyTransaction",)
