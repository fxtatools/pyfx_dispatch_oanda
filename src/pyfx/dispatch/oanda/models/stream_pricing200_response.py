
"""StreamPricing200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .client_price import StreamingPrice
from .pricing_heartbeat import PricingHeartbeat


class StreamPricing200Response(ApiObject):
    """
    The response body for the Pricing Stream uses chunked transfer encoding.  Each chunk contains Price and/or PricingHeartbeat objects encoded as JSON.  Each JSON object is serialized into a single line of text, and multiple objects found in the same chunk are separated by newlines. Heartbeats are sent every 5 seconds.
    """

    price: Annotated[Optional[StreamingPrice], TransportField(None)]
    """
    The specification of an Account-specific Price.
    """

    heartbeat: Annotated[Optional[PricingHeartbeat], TransportField(None)]
    """
    A PricingHeartbeat object is injected into the Pricing stream to ensure that the HTTP connection remains active.
    """


__all__ = ("StreamPricing200Response",)
