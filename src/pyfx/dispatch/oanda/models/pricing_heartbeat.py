"""PricingHeartbeat model definition for OANDA v20 Streaming API (3.0.25)"""

from typing import Annotated, Literal

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import Time


class PricingHeartbeat(ApiObject):
    """
    A PricingHeartbeat object is injected into the Pricing stream to ensure that the HTTP connection remains active.
    """

    type: Annotated[Literal["HEARTBEAT"], TransportField(...)] = "HEARTBEAT"
    """
    The string \"HEARTBEAT\"
    """

    time: Annotated[Time, TransportField(...)]
    """
    The date/time when the Heartbeat was created.
    """


__all__ = ("PricingHeartbeat",)
