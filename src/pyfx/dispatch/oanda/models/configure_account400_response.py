"""ConfigureAccount400Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport import TransportField
from .response_mixins import ErrorResponse
from .client_configure_reject_transaction import ClientConfigureRejectTransaction
from .common_types import TransactionId


class ConfigureAccount400Response(ErrorResponse):
    """
    Response status codes under ConfigureAccount400Response:
    400: The configuration specification was invalid.
    403: The configuration operation was forbidden on the Account.
    """

    client_configure_reject_transaction: Annotated[Optional[ClientConfigureRejectTransaction], TransportField(None, alias="clientConfigureRejectTransaction")]
    """
    The transaction that rejects the configuration of the Account.
    """

    last_transaction_id: Annotated[Optional[TransactionId], TransportField(None, alias="lastTransactionID")]
    """The ID of the last Transaction created for the Account.
    """


__all__ = ("ConfigureAccount400Response",)
