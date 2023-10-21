"""TransactionHeartbeat model definition for OANDA v20 Streaming API (3.0.25)"""

from typing import Annotated, Literal, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import Time, TransactionId

class TransactionHeartbeat(ApiObject):
    """
    A TransactionHeartbeat object is injected into the Transaction stream to ensure that the HTTP connection remains active.
    """

    type: Annotated[Literal["HEARTBEAT"], TransportField(None)] = "HEARTBEAT"
    """
    The string \"HEARTBEAT\"
    """

    last_transaction_id: Annotated[Optional[TransactionId], TransportField(..., alias="lastTransactionID")]
    """
    The ID of the most recent Transaction created for the Account
    """

    time: Annotated[Time, TransportField(...)]
    """
    The date/time when the TransactionHeartbeat was created.
    """


__all__ = ("TransactionHeartbeat",)
