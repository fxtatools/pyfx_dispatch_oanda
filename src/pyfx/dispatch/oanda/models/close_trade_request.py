"""CloseTradeRequest model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated
from numpy import double

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import DoubleConstants
from .transport_types import TransportDecmialAll


class CloseTradeRequest(ApiObject):
    """
    CloseTradeRequest
    """

    units: Annotated[double, TransportField(DoubleConstants.INF, transport_type=TransportDecmialAll)]
    """Indication of how much of the Trade to close.

    Either the string \"ALL\" (indicating that all of the Trade should be closed), or a DecimalNumber representing the number of units of the open Trade to Close using a TradeClose MarketOrder.

    The units specified must always be positive, and the magnitude of the value cannot exceed the magnitude of the Trade's open units.
    """


__all__ = ("CloseTradeRequest",)
