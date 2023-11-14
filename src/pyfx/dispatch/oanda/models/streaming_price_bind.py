"""Mapping definition for StreamingPriceObject

This module should be used for importing any of the following classes:
- StreamingPriceObject
- ClientPrice
- PricingHeartbeat
"""

from .streaming_price_base import StreamingPriceObject, StreamingPriceType
from .client_price import StreamingPrice
from .pricing_heartbeat import PricingHeartbeat


StreamingPriceObject.bind_types({
    StreamingPriceType.PRICE: StreamingPrice,
    StreamingPriceType.HEARTBEAT: PricingHeartbeat
})


__all__ = "StreamingPriceObject", "StreamingPriceType", "StreamingPrice", "PricingHeartbeat"
