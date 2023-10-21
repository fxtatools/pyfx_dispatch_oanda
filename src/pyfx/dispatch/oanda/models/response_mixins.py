"""Mixin classes for Response model classes"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import TransactionId


class Response(ApiObject):
    """Comon base class for response objects"""


class LastTransactionResponse(Response):
    """
    Mixin class for transaction-related response information
    """

    last_transaction_id: Annotated[TransactionId, TransportField(
        None, alias="lastTransactionID",
        description="The ID of the most recent Transaction created for the Account"
    )]


class TransactionResponse(LastTransactionResponse):
    """
    Mixin class for transaction-related response information with related transaction IDs
    """

    related_transaction_ids: Annotated[Optional[list[TransactionId]], TransportField(
        None, alias="relatedTransactionIDs",
        description="The IDs of all Transactions that were created while satisfying the request."
    )]


class ErrorResponse(Response):
    error_code: Annotated[Optional[int], TransportField(
        None,
        alias="errorCode",
        description="The code of the error that has occurred. This field may not be returned for some errors."
    )]

    error_message: Annotated[Optional[str], TransportField(
        None,
        alias="errorMessage",
        description="The human-readable description of the error that has occurred."
    )]


class TransactionErrorResponse(ErrorResponse, TransactionResponse):
    """
    Common base class for transaction-related error response models
    """


__all__ = ("TransactionResponse", "ErrorResponse", "TransactionErrorResponse",)
