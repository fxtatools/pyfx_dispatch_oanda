"""InstrumentsInstrumentOrderBookGet200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated

from .order_book import OrderBook

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField


class InstrumentsInstrumentOrderBookGet200Response(ApiObject):
    """
    InstrumentsInstrumentOrderBookGet200Response
    """
    order_book: Annotated[OrderBook, TransportField(..., alias="orderBook")]


__all__ = ("InstrumentsInstrumentOrderBookGet200Response",)
