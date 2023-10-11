"""Mixin classes for Response model classes"""

from typing import Optional

from ..util.naming import exporting

from ..transport import ApiObject, TransportField
from .common_types import TransactionId


class TransactionResponse(ApiObject):
    """
    Mixin class for transaction-related response information
    """

    related_transaction_ids: Optional[list[TransactionId]] = TransportField(
        None, alias="relatedTransactionIDs",
        description="The IDs of all Transactions that were created while satisfying the request."
    )

    last_transaction_id: Optional[TransactionId] = TransportField(
        None, alias="lastTransactionID",
        description="The ID of the most recent Transaction created for the Account"
    )


class ErrorResponse(ApiObject):
    error_code: Optional[int] = TransportField(
        None,
        alias="errorCode",
        description="The code of the error that has occurred. This field may not be returned for some errors."
    )

    error_message: Optional[str] = TransportField(
        None,
        alias="errorMessage",
        description="The human-readable description of the error that has occurred."
    )


class TransactionErrorResponse(ErrorResponse, TransactionResponse):
    """
    Common base class for transaction-related error response models
    """


__all__ = tuple(exporting(__name__, ...))
