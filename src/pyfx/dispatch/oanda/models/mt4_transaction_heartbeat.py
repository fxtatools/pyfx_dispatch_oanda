
"""model definition for OANDA v20 REST API (3.0.25)"""


from pandas import Timestamp


from typing import Optional


from ..transport import ApiObject, TransportField
from ..util import exporting


class MT4TransactionHeartbeat(ApiObject):
    """
    A TransactionHeartbeat object is injected into the Transaction stream to ensure that the HTTP connection remains active.
    """
    type: Optional[str] = TransportField(None)
    """
    The string \"HEARTBEAT\"
    """
    time: Timestamp = TransportField(None)
    """
    The date/time when the TransactionHeartbeat was created.
    """


__all__ = exporting(__name__, ...)
