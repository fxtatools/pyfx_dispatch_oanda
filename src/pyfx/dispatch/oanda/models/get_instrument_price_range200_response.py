"""GetInstrumentPriceRange200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .price import Price

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import Time

from .home_conversions import HomeConversions


class GetInstrumentPriceRange200Response(ApiObject):
    """
    GetInstrumentPriceRange200Response
    """

    prices: Annotated[Optional[list[Price]], TransportField(None)]
    """The list of prices that satisfy the request.
    """

    home_conversions: Annotated[Optional[list[HomeConversions]], TransportField(None, alias="homeConversions")]
    """
    The list of home currency conversion factors requested.

    This field will only be present if includeHomeConversions was set to true in the request.

    supplemental to the fxTrade v20 API 3.0.25
    """

    time : Annotated[Optional[Time], TransportField(...)]
    """The DateTime value to use for the "since" parameter in the next poll request.

    supplemental to the fxTrade v20 API 3.0.25
    """


__all__ =("GetInstrumentPriceRange200Response",)
