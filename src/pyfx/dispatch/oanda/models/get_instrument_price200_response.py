
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from .price import Price

from ..transport import ApiObject, TransportField
from ..util import exporting


class GetInstrumentPrice200Response(ApiObject):
    """
    GetInstrumentPrice200Response
    """
    price: Optional[Price] = TransportField(None)


__all__ = exporting(__name__, ...)
