"""TrailingStopLossDetails model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .client_extensions import ClientExtensions

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .time_in_force import TimeInForce

from .common_types import Time, PriceValue


class TrailingStopLossDetails(ApiObject):
    """TrailingStopLossDetails specifies the details of a Trailing Stop Loss Order to be created on behalf of a client.

    This may happen when an Order is filled that opens a Trade requiring a Trailing Stop Loss, or when a Trade's
    dependent Trailing Stop Loss Order is modified directly through the Trade.
    """

    distance: Annotated[PriceValue, TransportField(...)]
    """
    The distance (in price units) from the Trade's fill price that the Trailing Stop Loss Order will be triggered at.
    """

    time_in_force: Annotated[TimeInForce, TransportField(None, alias="timeInForce")] = TimeInForce.GTC
    """The time in force for the created Trailing Stop Loss Order.

    This may only be GTC, GTD or GFD.
    """

    gtd_time: Annotated[Optional[Time], TransportField(None, alias="gtdTime")]
    """The date when the Trailing Stop Loss Order will be cancelled on if timeInForce is GTD.
    """

    client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="clientExtensions")]
    """The Client Extensions to add to the Trailing Stop Loss Order when created.
    """


__all__ = ("TrailingStopLossDetails",)
