"""DailyFinancingTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional

from ..transport.transport_fields import TransportField

from .transaction import Transaction
from .transaction_type import TransactionType
from .common_types import AccountUnits
from .account_financing_mode import AccountFinancingMode
from .position_financing import PositionFinancing


class DailyFinancingTransaction(Transaction):
    """
    A DailyFinancingTransaction represents the daily payment/collection of financing for an Account.
    """

    type: Annotated[Literal[TransactionType.DAILY_FINANCING], TransportField(TransactionType.DAILY_FINANCING)] = TransactionType.DAILY_FINANCING
    """
    The Type of the Transaction. Always set to \"DAILY_FINANCING\" for a DailyFinancingTransaction.
    """

    financing: Annotated[Optional[AccountUnits], TransportField(None)]
    """
    The amount of financing paid/collected for the Account.
    """

    account_balance: Annotated[Optional[AccountUnits], TransportField(None, alias="accountBalance")]
    """
    The Account's balance after daily financing.
    """

    account_financing_mode: Annotated[Optional[AccountFinancingMode], TransportField(None, alias="accountFinancingMode", deprecated=True)]
    """
    The account financing mode at the time of the daily financing.
    """

    position_financings: Annotated[Optional[list[PositionFinancing]], TransportField(None, alias="positionFinancings")]
    """
    The financing paid/collected for each Position in the Account.
    """


__all__ = ("DailyFinancingTransaction",)
