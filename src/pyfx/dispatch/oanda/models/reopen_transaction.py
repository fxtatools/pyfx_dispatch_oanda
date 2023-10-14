
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport import TransportField

from .transaction import Transaction
from .transaction_type import TransactionType


class ReopenTransaction(Transaction):
    """
    A ReopenTransaction represents the re-opening of a closed Account.
    """

    type: Annotated[Literal[TransactionType.REOPEN], TransportField(TransactionType.REOPEN)] = TransactionType.REOPEN
    """
    The Type of the Transaction. Always set to \"REOPEN\" in a ReopenTransaction.
    """


__all__ = ("ReopenTransaction",)
