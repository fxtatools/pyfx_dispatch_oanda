
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from .position_book import PositionBook

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


class InstrumentsInstrumentPositionBookGet200Response(ApiObject):
    """
    InstrumentsInstrumentPositionBookGet200Response
    """
    position_book: Annotated[Optional[PositionBook], TransportField(None, alias="positionBook")]


__all__ = exporting(__name__, ...)
