
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from .price import Price


from ..transport import ApiObject, TransportField
from ..util import exporting


class GetInstrumentPriceRange200Response(ApiObject):
    """
    GetInstrumentPriceRange200Response
    """
    prices: Optional[list[Price]] = TransportField(None)
    """The list of prices that satisfy the request.
    """


__all__ = exporting(__name__, ...)
