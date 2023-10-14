
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from .price import Price


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


class GetInstrumentPriceRange200Response(ApiObject):
    """
    GetInstrumentPriceRange200Response
    """
    prices: Annotated[Optional[list[Price]], TransportField(None)]
    """The list of prices that satisfy the request.
    """


__all__ = exporting(__name__, ...)
