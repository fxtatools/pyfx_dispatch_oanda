"""MarginCallExitTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal

from ..transport import TransportField

from .transaction import Transaction
from .transaction_type import TransactionType


class MarginCallExitTransaction(Transaction):
    """
    A MarginCallExitnterTransaction is created when an Account leaves the margin call state.
    """

    type: Literal[TransactionType.MARGIN_CALL_EXIT] = TransportField(TransactionType.MARGIN_CALL_EXIT)
    """
    The Type of the Transaction. Always set to \"MARGIN_CALL_EXIT\" for an MarginCallExitTransaction.
    """


__all__ = ("MarginCallExitTransaction",)
