"""Transaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport import AbstractApiObject, TransportField

from .common_types import TransactionId, AccountId, ClientRequestId, Time
from .transaction_type import TransactionType


class Transaction(AbstractApiObject,
                  designator_key="type",
                  designator_type=TransactionType):
    """
    The base Transaction specification.
    """

    id: TransactionId = TransportField(...)
    """
    The Transaction's Identifier.
    """

    time: Time = TransportField(...)
    """
    The date/time when the Transaction was created.
    """

    user_id: int = TransportField(..., alias="userID")
    """
    The ID of the user that initiated the creation of the Transaction.
    """

    account_id: AccountId = TransportField(..., alias="accountID")
    """
    The ID of the Account the Transaction was created for.
    """

    batch_id: TransactionId = TransportField(..., alias="batchID")
    """
    The ID of the \"batch\" that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously.
    """

    request_id: Optional[ClientRequestId] = TransportField(None, alias="requestID")
    """
    The Request ID of the request which generated the transaction.
    """


__all__ = ("Transaction",)
