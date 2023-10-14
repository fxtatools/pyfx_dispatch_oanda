
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from .order_book import OrderBook

from ..transport import ApiObject, TransportField
from ..util import exporting


class InstrumentsInstrumentOrderBookGet200Response(ApiObject):
    """
    InstrumentsInstrumentOrderBookGet200Response
    """
    order_book: Annotated[Optional[OrderBook], TransportField(None, alias="orderBook")]


__all__ = exporting(__name__, ...)
