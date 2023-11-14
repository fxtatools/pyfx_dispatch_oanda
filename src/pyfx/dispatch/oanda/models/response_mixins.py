"""Mixin classes for Response model classes"""

from abc import ABC
from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import TransactionId


class ApiResponse(ApiObject, ABC):
    """Comon base class for API response objects"""


class LastTransactionResponse(ApiResponse, ABC):
    """
    Mixin class for transaction-related response information
    """

    last_transaction_id: Annotated[TransactionId, TransportField(
        None, alias="lastTransactionID",
        description="The ID of the most recent Transaction created for the Account"
    )]


class TransactionResponse(LastTransactionResponse, ABC):
    """
    Mixin class for transaction-related response information with related transaction IDs
    """

    related_transaction_ids: Annotated[Optional[list[TransactionId]], TransportField(
        None, alias="relatedTransactionIDs",
        description="The IDs of all Transactions that were created while satisfying the request."
    )]


class ErrorResponse(ApiResponse, ABC):
    error_code: Annotated[Optional[int], TransportField(
        None,
        alias="errorCode",
        description="The code of the error that has occurred. This field may not be returned for some errors."
    )]


class ApiErrorResponse(ApiResponse, ABC):
    error_message: Annotated[Optional[str], TransportField(
        None,
        alias="errorMessage",
        description="The human-readable description of the error that has occurred."
    )]


class TransactionErrorResponse(ApiErrorResponse, TransactionResponse, ABC):
    """
    Common base class for transaction-related error response models
    """


class UnknownErrorResponse(ErrorResponse, ABC):
    """Base class for unexpected error responses"""
    reason: Annotated[str, TransportField(
        ..., description="Response reason phrase"
    )]
    content_type: Annotated[str, TransportField(
        ..., description="Content type for the error response"
    )]
    content: Annotated[str, TransportField(
        ..., description="Content of the error response"
    )]


__all__ = (
    "ApiResponse", "LastTransactionResponse", "TransactionResponse",
    "ApiErrorResponse", "TransactionErrorResponse",  "UnknownErrorResponse"
)
