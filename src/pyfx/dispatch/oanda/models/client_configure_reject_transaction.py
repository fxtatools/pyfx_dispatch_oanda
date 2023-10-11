
"""ClientConfigureRejectTransaction model definition for OANDA v20 REST API (3.0.25)"""

from pandas import Timestamp

from typing import Literal, Optional

from ..transport import ApiObject, TransportField
from ..util import exporting

from .transaction_type import TransactionType
from .transaction_reject_reason import TransactionRejectReason


class ClientConfigureRejectTransaction(ApiObject):
    """
    A ClientConfigureRejectTransaction represents the reject of configuration of an Account by a client.
    """
    id: Optional[str] = TransportField(None)
    """The Transaction's Identifier.
    """
    time: Timestamp = TransportField(None)
    """The date/time when the Transaction was created.
    """
    user_id: Optional[int] = TransportField(None, alias="userID")
    """The ID of the user that initiated the creation of the Transaction.
    """
    account_id: Optional[str] = TransportField(None, alias="accountID")
    """The ID of the Account the Transaction was created for.
    """
    batch_id: Optional[str] = TransportField(None, alias="batchID")
    """The ID of the \"batch\" that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously.
    """
    request_id: Optional[str] = TransportField(None, alias="requestID")
    """The Request ID of the request which generated the transaction.
    """
    type: Literal[TransactionType.CLIENT_CONFIGURE_REJECT] = TransportField(Literal[TransactionType.CLIENT_CONFIGURE_REJECT])
    """The Type of the Transaction. Always set to \"CLIENT_CONFIGURE_REJECT\" in a ClientConfigureRejectTransaction.
    """
    alias: Optional[str] = TransportField(None)
    """The client-provided alias for the Account.
    """
    margin_rate: Optional[str] = TransportField(None, alias="marginRate")
    """The margin rate override for the Account.
    """
    reject_reason: Optional[TransactionRejectReason] = TransportField(None, alias="rejectReason")
    """The reason that the Reject Transaction was created
    """


__all__ = exporting(__name__, ...)
