
"""ClientConfigureTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal, Optional

from ..transport import TransportField

from .transaction_type import TransactionType
from .transaction import Transaction
from .common_types import FloatValue


class ClientConfigureTransaction(Transaction):
    """
    A ClientConfigureTransaction represents the configuration of an Account by a client.
    """

    type: Literal[TransactionType.CLIENT_CONFIGURE] = TransportField(TransactionType.CLIENT_CONFIGURE)
    """
    The Type of the Transaction. Always set to \"CLIENT_CONFIGURE\" in a ClientConfigureTransaction.
    """

    alias: Optional[str] = TransportField(None,)
    """
    The client-provided alias for the Account.
    """

    margin_rate: Optional[FloatValue] = TransportField(None,alias="marginRate",)
    """
    The margin rate override for the Account.
    """


__all__ = ("ClientConfigureTransaction",)
