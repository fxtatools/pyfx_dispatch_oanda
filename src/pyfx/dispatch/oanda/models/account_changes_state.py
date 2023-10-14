
"""AccountChangesState model definition for OANDA v20 REST API (3.0.25)"""

from pandas import Timestamp
from typing import Annotated, Optional

from .calculated_position_state import CalculatedPositionState
from .calculated_trade_state import CalculatedTradeState
from .dynamic_order_state import DynamicOrderState

from ..transport import TransportField

from .account_mixins import AccountStateBase


class AccountChangesState(AccountStateBase):
    """
    An AccountState Object is used to represent an Account's current price-dependent state. Price-dependent Account state is dependent on OANDA's current Prices, and includes things like unrealized PL, NAV and Trailing Stop Loss Order state.
    """

    orders: Annotated[Optional[list[DynamicOrderState]], TransportField(None)]
    """The price-dependent state of each pending Order in the Account.
    """
    
    trades: Annotated[Optional[list[CalculatedTradeState]], TransportField(None)]
    """The price-dependent state for each open Trade in the Account.
    """
    
    positions: Annotated[Optional[list[CalculatedPositionState]], TransportField(None)]
    """The price-dependent state for each open Position in the Account.
    """


__all__ = ("AccountChangesState",)
