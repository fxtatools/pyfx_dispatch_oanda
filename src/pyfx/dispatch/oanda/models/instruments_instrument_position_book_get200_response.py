"""InstrumentsInstrumentPositionBookGet200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated

from .position_book import PositionBook

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField


class InstrumentsInstrumentPositionBookGet200Response(ApiObject):
    """
    InstrumentsInstrumentPositionBookGet200Response
    """
    position_book: Annotated[PositionBook, TransportField(..., alias="positionBook")]


__all__ = ("InstrumentsInstrumentPositionBookGet200Response",)
