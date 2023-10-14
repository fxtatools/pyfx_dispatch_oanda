"""MarginCallEnterTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal

from ..transport import TransportField

from .transaction import Transaction
from .transaction_type import TransactionType


class MarginCallEnterTransaction(Transaction):
    """
    A MarginCallEnterTransaction is created when an Account enters the margin call state.
    """

    type: Annotated[Literal[TransactionType.MARGIN_CALL_ENTER], TransportField(TransactionType.MARGIN_CALL_ENTER)] = TransactionType.MARGIN_CALL_ENTER
    """
    The Type of the Transaction. Always set to \"MARGIN_CALL_ENTER\" for an MarginCallEnterTransaction.
    """


__all__ = ("MarginCallEnterTransaction",)
