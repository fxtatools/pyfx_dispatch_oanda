"""GetInstrumentPrice200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport import ApiObject, TransportField

from .price import Price


class GetInstrumentPrice200Response(ApiObject):
    """
    GetInstrumentPrice200Response
    """
    price: Optional[Price] = TransportField(None)


__all__ = ("GetInstrumentPrice200Response",)
