"""ClientConfigureRejectTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport.transport_fields import TransportField

from .transaction_type import TransactionType

from .transaction_mixins import RejectTxn
from .client_configure_transaction import ClientConfigureTransaction


class ClientConfigureRejectTransaction(RejectTxn, ClientConfigureTransaction):
    """
    A ClientConfigureRejectTransaction represents the reject of configuration of an Account by a client.
    """

    type: Annotated[Literal[TransactionType.CLIENT_CONFIGURE_REJECT], TransportField(Literal[TransactionType.CLIENT_CONFIGURE_REJECT])] = TransactionType.CLIENT_CONFIGURE_REJECT
    """The Type of the Transaction. Always set to \"CLIENT_CONFIGURE_REJECT\" in a ClientConfigureRejectTransaction.
    """


__all__ = ("ClientConfigureRejectTransaction",)
