"""MT4TransactionHeartbeat model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport import ApiObject, TransportField
from .common_types import Time


class MT4TransactionHeartbeat(ApiObject):
    """
    A TransactionHeartbeat object is injected into the Transaction stream to ensure that the HTTP connection remains active.

    This class was defined in the v20 REST API 3.0.25. In its present release, the documentation for the fxTrade API does not describe any usage for this class.
    """

    type: Optional[str] = TransportField(None)
    """
    The string \"HEARTBEAT\"
    """

    time: Time = TransportField(None)
    """
    The date/time when the TransactionHeartbeat was created.
    """


__all__ = ("MT4TransactionHeartbeat",)
