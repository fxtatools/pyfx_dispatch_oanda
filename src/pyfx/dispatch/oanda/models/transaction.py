"""Transaction model definition for OANDA v20 REST and Streaming APIs (3.0.25)"""

from BTrees import IOBTree
from persistent import Persistent

from typing import Annotated, Optional

from ..transport import AbstractApiObject, TransportField  # type: ignore[attr-defined]

from .common_types import TransactionId, AccountId, ClientRequestId, Time
from .transaction_type import TransactionType


class Transaction(AbstractApiObject,
                  designator_key="type",
                  designator_type=TransactionType):  # type: ignore[call-arg]
    """
    The base Transaction specification.
    """

    id: Annotated[TransactionId, TransportField(...)]
    """
    The Transaction's Identifier.
    """

    time: Annotated[Time, TransportField(...)]
    """
    The date/time when the Transaction was created.
    """

    user_id: Annotated[Optional[int], TransportField(None, alias="userID")]
    """
    The ID of the user that initiated the creation of the Transaction.
    """

    account_id: Annotated[AccountId, TransportField(..., alias="accountID")]
    """
    The ID of the Account the Transaction was created for.
    """

    batch_id: Annotated[TransactionId, TransportField(..., alias="batchID")]
    """
    The ID of the \"batch\" that the Transaction belongs to. Transactions in the same batch are applied to the Account simultaneously.
    """

    request_id: Annotated[Optional[ClientRequestId], TransportField(None, alias="requestID")]
    """
    The Request ID of the request which generated the transaction.
    """

    def get_btree(self):
        ## https://zodb.org/en/latest/guide/writing-persistent-objects.html#using-persistent-data-structures

        return IOBTree.BTree()

    def persist(self, dest: Persistent):
        dest[self.id] = self


__all__ = ("Transaction",)
