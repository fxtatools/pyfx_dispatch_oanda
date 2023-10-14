
"""Account model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport import TransportField

from .account_mixins import AccountSummaryBase
from .order import Order
from .position import Position
from .trade_summary import TradeSummary
from .common_types import TransactionId


class Account(AccountSummaryBase):
    """
    The full details of a client's Account. This includes full open Trade, open Position and pending Order representation.
    """

    last_transaction_id: Annotated[Optional[TransactionId], TransportField(None, alias="lastTransactionID")]
    """The ID of the last Transaction created for the Account.
    """

    trades: Annotated[Optional[list[TradeSummary]], TransportField(None)]
    """The details of the Trades currently open in the Account.
    """

    positions: Annotated[Optional[list[Position]], TransportField(None)]
    """The details all Account Positions.
    """

    orders: Annotated[Optional[list[Order]], TransportField(None)]
    """The details of the Orders currently pending in the Account.
    """


__all__ = ("Account",)
