
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from .position_book import PositionBook

from ..transport import ApiObject, TransportField
from ..util import exporting


class InstrumentsInstrumentPositionBookGet200Response(ApiObject):
    """
    InstrumentsInstrumentPositionBookGet200Response
    """
    position_book: Optional[PositionBook] = TransportField(None, alias="positionBook")


__all__ = exporting(__name__, ...)
