"""MT4TransactionHeartbeat model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import Time


class MT4TransactionHeartbeat(ApiObject):
    """
    A TransactionHeartbeat object is injected into the Transaction stream to ensure that the HTTP connection remains active.

    [**Deprecated**]

    This class was produced from definitions in the fxTrade v20 API 3.0.25.

    In its present release, the documentation for the fxTrade API does not describe any usage for this class.
    """

    type: Annotated[Literal["HEARTBEAT"], TransportField(None)] = "HEARTBEAT"
    """
    The string \"HEARTBEAT\"
    """

    time: Annotated[Time, TransportField(...)]
    """
    The date/time when the TransactionHeartbeat was created.
    """


__all__ = ("MT4TransactionHeartbeat",)
