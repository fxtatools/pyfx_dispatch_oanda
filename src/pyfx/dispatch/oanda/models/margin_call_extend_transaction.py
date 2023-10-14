"""MarginCallExtendTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional

from ..transport import TransportField

from .transaction import Transaction
from .transaction_type import TransactionType


class MarginCallExtendTransaction(Transaction):
    """
    A MarginCallExtendTransaction is created when the margin call state for an Account has been extended.
    """

    type: Annotated[Literal[TransactionType.MARGIN_CALL_EXTEND], TransportField(TransactionType.MARGIN_CALL_EXTEND)] = TransactionType.MARGIN_CALL_EXTEND
    """
    The Type of the Transaction. Always set to \"MARGIN_CALL_EXTEND\" for an MarginCallExtendTransaction.
    """

    extension_number: Annotated[Optional[int], TransportField(None, alias="extensionNumber")]
    """
    The number of the extensions to the Account's current margin call that have been applied. This value will be set to 1 for the first MarginCallExtend Transaction
    """


__all__ = ("MarginCallExtendTransaction",)
