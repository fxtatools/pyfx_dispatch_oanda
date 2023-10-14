
"""ClientConfigureTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional

from ..transport.transport_fields import TransportField

from .transaction_type import TransactionType
from .transaction import Transaction
from .common_types import FloatValue


class ClientConfigureTransaction(Transaction):
    """
    A ClientConfigureTransaction represents the configuration of an Account by a client.
    """

    type: Annotated[Literal[TransactionType.CLIENT_CONFIGURE], TransportField(TransactionType.CLIENT_CONFIGURE)] = TransactionType.CLIENT_CONFIGURE
    """
    The Type of the Transaction. Always set to \"CLIENT_CONFIGURE\" in a ClientConfigureTransaction.
    """

    alias: Annotated[Optional[str], TransportField(None,)]
    """
    The client-provided alias for the Account.
    """

    margin_rate: Annotated[Optional[FloatValue], TransportField(None,alias="marginRate",)]
    """
    The margin rate override for the Account.
    """


__all__ = ("ClientConfigureTransaction",)
