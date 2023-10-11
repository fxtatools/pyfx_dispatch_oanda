
"""PositionSide model for OANDA v20 REST API (3.0.25)"""

from numpy import abs, double, sign
from typing import Optional

from ..transport import ApiObject, TransportField

from .common_types import AccountUnits, PriceValue, LotsValue, TradeId, FloatValue


class PositionSide(ApiObject):
    """
    The representation of a Position for a single direction (long or short).
    """

    units: LotsValue = TransportField(...)
    """
    Number of units in the position (negative value indicates short position, positive indicates long position).
    """

    average_price: Optional[PriceValue] = TransportField(None, alias="averagePrice")
    """
    Volume-weighted average of the underlying Trade open prices for the Position.
    """

    trade_ids: Optional[list[TradeId]] = TransportField(None, alias="tradeIDs")
    """
    List of the open Trade IDs which contribute to the open Position.
    """

    pl: Optional[AccountUnits] = TransportField(None)
    """
    Profit/loss realized by the PositionSide over the lifetime of the Account.
    """

    unrealized_pl: Optional[AccountUnits] = TransportField(None, alias="unrealizedPL")
    """
    The unrealized profit/loss of all open Trades that contribute to this PositionSide.
    """

    resettable_pl: Optional[AccountUnits] = TransportField(None, alias="resettablePL")
    """
    Profit/loss realized by the PositionSide since the Account's resettablePL was last reset by the client.
    """

    financing: Optional[AccountUnits] = TransportField(None)
    """
    The total amount of financing paid/collected for this PositionSide over the lifetime of the Account.
    """

    guaranteed_execution_fees: Optional[AccountUnits] = TransportField(None, alias="guaranteedExecutionFees")
    """
    The total amount of fees charged over the lifetime of the Account for the execution of guaranteed Stop Loss Orders attached to Trades for this PositionSide.
    """

    def is_short_position(self) -> bool:
        """Return true if this PositionSide represents a short position"""
        return sign(self.units) == -1

    def is_long_position(self) -> bool:
        """Return true if this PositionSide represents a long position"""
        return sign(self.units) == 1

    def abs_units(self) -> double:
        """Return the absolute value for this position"""
        return abs(self.units)

__all__ = ("PositionSide",)
