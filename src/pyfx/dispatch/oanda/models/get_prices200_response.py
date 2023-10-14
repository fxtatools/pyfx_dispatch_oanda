
"""model definition for OANDA v20 REST API (3.0.25)"""


from pandas import Timestamp


from typing import Annotated, Optional

from .client_price import ClientPrice
from .home_conversions import HomeConversions


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


class GetPrices200Response(ApiObject):
    """
    GetPrices200Response
    """
    prices: Annotated[Optional[list[ClientPrice]], TransportField(None)]
    """
    The list of Price objects requested.
    """
    home_conversions: Annotated[Optional[list[HomeConversions]], TransportField(None, alias="homeConversions")]
    """
    The list of home currency conversion factors requested. This field will only be present if includeHomeConversions was set to true in the request.
    """
    time: Annotated[Timestamp, TransportField(None)]
    """
    The DateTime value to use for the \"since\" parameter in the next poll request.
    """


__all__ = exporting(__name__, ...)
