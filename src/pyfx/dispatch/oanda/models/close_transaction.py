"""CloseTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal

from ..transport import TransportField

from .transaction import Transaction
from .transaction_type import TransactionType


class CloseTransaction(Transaction):
    """
    A CloseTransaction represents the closing of an Account.
    """

    type: Literal[TransactionType.CLOSE] = TransportField(TransactionType.CLOSE)
    """
    The Type of the Transaction. Always set to \"CLOSE\" in a CloseTransaction.
    """


__all__ = ("CloseTransaction",)
