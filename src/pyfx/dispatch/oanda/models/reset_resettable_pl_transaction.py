"""ResetResettablePLTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport import TransportField

from .transaction import Transaction
from .transaction_type import TransactionType


class ResetResettablePLTransaction(Transaction):
    """
    A ResetResettablePLTransaction represents the resetting of the Account's resettable PL counters.
    """

    type: Annotated[Literal[TransactionType.RESET_RESETTABLE_PL], TransportField(TransactionType.RESET_RESETTABLE_PL)] = TransactionType.RESET_RESETTABLE_PL
    """
    The Type of the Transaction. Always set to \"RESET_RESETTABLE_PL\" for a ResetResettablePLTransaction.
    """


__all__ = ("ResetResettablePLTransaction",)
