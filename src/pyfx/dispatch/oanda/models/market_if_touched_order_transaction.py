
"""MarketIfTouchedOrderTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport import TransportField

from .transaction_mixins import PriceBoundEntryTransaction
from .transaction_type import TransactionType
from .common_types import PriceValue
from .time_in_force import TimeInForce


class MarketIfTouchedOrderTransaction(PriceBoundEntryTransaction):
    """
    A MarketIfTouchedOrderTransaction represents the creation of a MarketIfTouched Order in the user's Account.
    """

    type: Annotated[Literal[TransactionType.MARKET_IF_TOUCHED_ORDER], TransportField(TransactionType.MARKET_IF_TOUCHED_ORDER)] = TransactionType.MARKET_IF_TOUCHED_ORDER
    """
    The Type of the Transaction. Always set to \"MARKET_IF_TOUCHED_ORDER\" in a MarketIfTouchedOrderTransaction.
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price threshold specified for the MarketIfTouched Order. The MarketIfTouched Order will only be filled by a market price that crosses this price from the direction of the market price at the time when the Order was created (the initialMarketPrice). Depending on the value of the Order's price and initialMarketPrice, the MarketIfTouchedOrder will behave like a Limit or a Stop Order.
    """

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.GTC, alias="timeInForce")]
    """
    The time-in-force requested for the MarketIfTouched Order. Restricted to \"GTC\", \"GFD\" and \"GTD\" for MarketIfTouched Orders.
    """


__all__ = ("MarketIfTouchedOrderTransaction",)
