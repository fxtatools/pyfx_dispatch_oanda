"""GetInstrumentPrice200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport import ApiObject, TransportField

from .price import Price


class GetInstrumentPrice200Response(ApiObject):
    """
    GetInstrumentPrice200Response
    """
    price: Annotated[Optional[Price], TransportField(None)]


__all__ = ("GetInstrumentPrice200Response",)
