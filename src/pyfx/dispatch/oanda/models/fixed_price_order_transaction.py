"""FixedPriceOrderTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional

from ..transport.transport_fields import TransportField

from .transaction_mixins import OrderFillTxn, ClientExtensionsTxn
from .transaction_type import TransactionType

from .common_types import PriceValue
from .fixed_price_order_reason import FixedPriceOrderReason


class FixedPriceOrderTransaction(OrderFillTxn, ClientExtensionsTxn):
    """
    A FixedPriceOrderTransaction represents the creation of a Fixed Price Order in the user's account. A Fixed Price Order is an Order that is filled immediately at a specified price.
    """

    type: Annotated[Literal[TransactionType.FIXED_PRICE_ORDER], TransportField(TransactionType.FIXED_PRICE_ORDER)] = TransactionType.FIXED_PRICE_ORDER
    """
    The Type of the Transaction. Always set to \"FIXED_PRICE_ORDER\
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price specified for the Fixed Price Order. This price is the exact price that the Fixed Price Order will be filled at.
    """

    trade_state: Annotated[str, TransportField(..., alias="tradeState")]
    """
    The state that the trade resulting from the Fixed Price Order should be set to.
    """

    reason: Annotated[Optional[FixedPriceOrderReason], TransportField(None)]
    """
    The reason that the Fixed Price Order was created
    """


__all__ = ("FixedPriceOrderTransaction",)
