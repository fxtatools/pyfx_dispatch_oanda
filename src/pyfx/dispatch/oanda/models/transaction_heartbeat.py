
"""model definition for OANDA v20 REST API (3.0.25)"""


from pandas import Timestamp






from typing import Annotated, Optional



from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting



class TransactionHeartbeat(ApiObject):
    """
    A TransactionHeartbeat object is injected into the Transaction stream to ensure that the HTTP connection remains active.
    """
    type: Annotated[Optional[str], TransportField(None)]
    """
    The string \"HEARTBEAT\"
    """
    last_transaction_id: Annotated[Optional[str], TransportField(None, alias="lastTransactionID")]
    """
    The ID of the most recent Transaction created for the Account
    """
    time: Annotated[Timestamp, TransportField(None)]
    """
    The date/time when the TransactionHeartbeat was created.
    """


__all__ = exporting(__name__, ...)

