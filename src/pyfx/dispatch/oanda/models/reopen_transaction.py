
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal

from ..transport import TransportField

from .transaction import Transaction
from .transaction_type import TransactionType


class ReopenTransaction(Transaction):
    """
    A ReopenTransaction represents the re-opening of a closed Account.
    """

    type: Literal[TransactionType.REOPEN] = TransportField(TransactionType.REOPEN)
    """
    The Type of the Transaction. Always set to \"REOPEN\" in a ReopenTransaction.
    """


__all__ = ("ReopenTransaction",)
