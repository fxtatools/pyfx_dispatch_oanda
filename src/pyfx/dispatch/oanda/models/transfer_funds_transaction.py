
"""TransferFundsTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional

from ..transport import TransportField

from .transaction import Transaction
from .transaction_type import TransactionType
from .funding_reason import FundingReason
from .common_types import AccountUnits


class TransferFundsTransaction(Transaction):
    """
    A TransferFundsTransaction represents the transfer of funds in/out of an Account.
    """

    type: Annotated[Literal[TransactionType.TRANSFER_FUNDS], TransportField(TransactionType.TRANSFER_FUNDS)] = TransactionType.TRANSFER_FUNDS
    """
    The Type of the Transaction. Always set to \"TRANSFER_FUNDS\" in a TransferFundsTransaction.
    """

    amount: Annotated[Optional[AccountUnits], TransportField(None)]
    """
    The amount to deposit/withdraw from the Account in the Account's home currency. A positive value indicates a deposit, a negative value indicates a withdrawal.
    """

    funding_reason: Annotated[Optional[FundingReason], TransportField(None, alias="fundingReason")]
    """
    The reason that an Account is being funded.
    """

    comment: Annotated[Optional[str], TransportField(None)]
    """
    An optional comment that may be attached to a fund transfer for audit purposes
    """

    account_balance: Annotated[Optional[AccountUnits], TransportField(None, alias="accountBalance")]
    """
    The Account's balance after funds are transferred.
    """


__all__ = ("TransferFundsTransaction",)
