
"""model definition for OANDA v20 REST API (3.0.25)"""


from pandas import Timestamp


from typing import Annotated, Optional


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


class PricingHeartbeat(ApiObject):
    """
    A PricingHeartbeat object is injected into the Pricing stream to ensure that the HTTP connection remains active.
    """
    type: Annotated[Optional[str], TransportField(None)]
    """
    The string \"HEARTBEAT\"
    """
    time: Annotated[Timestamp, TransportField(None)]
    """
    The date/time when the Heartbeat was created.
    """


__all__ = exporting(__name__, ...)
