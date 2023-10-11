
"""TransferFundsRejectTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal

from ..transport import TransportField

from .transfer_funds_transaction import TransferFundsTransaction
from .transaction_mixins import RejectTxn
from .transaction_type import TransactionType


class TransferFundsRejectTransaction(RejectTxn, TransferFundsTransaction):
    """
    A TransferFundsRejectTransaction represents the rejection of the transfer of funds in/out of an Account.
    """

    type: Literal[TransactionType.TRANSFER_FUNDS_REJECT] = TransportField(TransactionType.TRANSFER_FUNDS_REJECT)
    """
    The Type of the Transaction. Always set to \"TRANSFER_FUNDS_REJECT\" in a TransferFundsRejectTransaction.
    """


__all__ = ("TransferFundsRejectTransaction",)
