
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from .common_types import AccountUnits
from .position_side import PositionSide

from ..transport import ApiObject, TransportField


class Position(ApiObject):
    """
    The specification of a Position within an Account.
    """
    instrument: Optional[str] = TransportField(None)
    """
    The Position's Instrument.
    """
    pl: Optional[AccountUnits] = TransportField(None)
    """
    Profit/loss realized by the Position over the lifetime of the Account.
    """
    unrealized_pl: Optional[AccountUnits] = TransportField(None, alias="unrealizedPL")
    """
    The unrealized profit/loss of all open Trades that contribute to this Position.
    """
    margin_used: Optional[AccountUnits] = TransportField(None, alias="marginUsed")
    """
    Margin currently used by the Position.
    """
    resettable_pl: Optional[AccountUnits] = TransportField(None, alias="resettablePL")
    """
    Profit/loss realized by the Position since the Account's resettablePL was last reset by the client.
    """
    financing: Optional[AccountUnits] = TransportField(None)
    """
    The total amount of financing paid/collected for this instrument over the lifetime of the Account.
    """
    commission: Optional[AccountUnits] = TransportField(None)
    """
    The total amount of commission paid for this instrument over the lifetime of the Account.
    """
    guaranteed_execution_fees: Optional[AccountUnits] = TransportField(None, alias="guaranteedExecutionFees")
    """
    The total amount of fees charged over the lifetime of the Account for the execution of guaranteed Stop Loss Orders for this instrument.
    """
    long: Optional[PositionSide] = TransportField(None)
    """
    The details of the long side of the Position.
    """
    short: Optional[PositionSide] = TransportField(None)
    """
    The details of the short side of the Position.
    """


__all__ = ("Position",)
