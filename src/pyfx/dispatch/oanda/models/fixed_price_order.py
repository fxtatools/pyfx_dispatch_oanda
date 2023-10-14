"""FixedPriceOrder model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Literal

from ..transport import TransportField

from .order_mixins import UnitsOrderBase

from .order_type import OrderType
from .common_types import PriceValue


class FixedPriceOrder(UnitsOrderBase):
    """
    A FixedPriceOrder is an order that is filled immediately upon creation using a fixed price.
    """

    type: Annotated[Literal[OrderType.FIXED_PRICE], TransportField(OrderType.FIXED_PRICE)] = OrderType.FIXED_PRICE
    """
    The type of the Order. Always set to “FIXED_PRICE” for Fixed Price Orders.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price specified for the Fixed Price Order. This price is the exact price that the Fixed Price Order will be filled at.
    """

    trade_state: Annotated[str, TransportField(..., alias="tradeState")]
    # TBD: The documentation specifies an unconstrained string type for this field
    # https://developer.oanda.com/rest-live-v20/order-df/#FixedPriceOrder
    """
    The state that the trade resulting from the Fixed Price Order should be set to.
    """


__all__ = ("FixedPriceOrder",)
