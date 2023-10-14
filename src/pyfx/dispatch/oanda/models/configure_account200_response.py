"""ConfigureAccount200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport import ApiObject, TransportField

from .client_configure_transaction import ClientConfigureTransaction
from .common_types import TransactionId


class ConfigureAccount200Response(ApiObject):
    """
    ConfigureAccount200Response:  The Account was configured successfully
    """
    client_configure_transaction: Annotated[Optional[ClientConfigureTransaction], TransportField(None, alias="clientConfigureTransaction")]

    last_transaction_id: Annotated[Optional[TransactionId], TransportField(None, alias="lastTransactionID")]
    """The ID of the last Transaction created for the Account.
    """


__all__ = ("ConfigureAccount200Response",)
