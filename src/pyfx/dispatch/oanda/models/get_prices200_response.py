"""GetPrices200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.transport_fields import TransportField

from .response_mixins import ApiResponse
from .client_price import StreamingPrice
from .home_conversions import HomeConversions
from .common_types import Time


class GetPrices200Response(ApiResponse):
    """
    GetPrices200Response
    """

    prices: Annotated[list[StreamingPrice], TransportField(...)]
    """
    The list of Price objects requested.
    """

    home_conversions: Annotated[Optional[list[HomeConversions]], TransportField(None, alias="homeConversions")]
    """
    The list of home currency conversion factors requested. This field will only be present if includeHomeConversions was set to true in the request.
    """

    time: Annotated[Time, TransportField(...)]
    """
    The DateTime value to use for the \"since\" parameter in the next poll request.
    """


__all__ = ("GetPrices200Response",)
