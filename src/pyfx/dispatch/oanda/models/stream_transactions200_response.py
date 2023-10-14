
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Annotated, Optional


from .transaction import Transaction
from .transaction_heartbeat import TransactionHeartbeat

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting



class StreamTransactions200Response(ApiObject):
    """
    The response body for the Transaction Stream uses chunked transfer encoding.  Each chunk contains Transaction and/or TransactionHeartbeat objects encoded as JSON.  Each JSON object is serialized into a single line of text, and multiple objects found in the same chunk are separated by newlines. TransactionHeartbeats are sent every 5 seconds.
    """

    transaction: Annotated[Optional[Transaction], TransportField(None)]
    """
    The base Transaction specification. Specifies properties that are common between all Transaction.
    """
    heartbeat: Annotated[Optional[TransactionHeartbeat], TransportField(None)]
    """
    A TransactionHeartbeat object is injected into the Transaction stream to ensure that the HTTP connection remains active.
    """


__all__ = exporting(__name__, ...)

