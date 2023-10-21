"""GetInstrumentPrice200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .price import Price


class GetInstrumentPrice200Response(ApiObject):
    """
    GetInstrumentPrice200Response

    [**Deprecated**]

    This class was defined for an API endpoint in the fxTrade v20 API 3.0.25.
    That endpoint may have been deprecated

    See also:
    - DefaultApi.get_prices()
    """
    price: Annotated[Optional[Price], TransportField(None)]


__all__ = ("GetInstrumentPrice200Response",)
