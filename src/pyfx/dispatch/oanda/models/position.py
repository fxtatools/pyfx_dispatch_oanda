
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .common_types import AccountUnits
from .position_side import PositionSide

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField


class Position(ApiObject):
    """
    The specification of a Position within an Account.
    """
    instrument: Annotated[Optional[str], TransportField(None)]
    """
    The Position's Instrument.
    """
    pl: Annotated[Optional[AccountUnits], TransportField(None)]
    """
    Profit/loss realized by the Position over the lifetime of the Account.
    """
    unrealized_pl: Annotated[Optional[AccountUnits], TransportField(None, alias="unrealizedPL")]
    """
    The unrealized profit/loss of all open Trades that contribute to this Position.
    """
    margin_used: Annotated[Optional[AccountUnits], TransportField(None, alias="marginUsed")]
    """
    Margin currently used by the Position.
    """
    resettable_pl: Annotated[Optional[AccountUnits], TransportField(None, alias="resettablePL")]
    """
    Profit/loss realized by the Position since the Account's resettablePL was last reset by the client.
    """
    financing: Annotated[Optional[AccountUnits], TransportField(None)]
    """
    The total amount of financing paid/collected for this instrument over the lifetime of the Account.
    """
    commission: Annotated[Optional[AccountUnits], TransportField(None)]
    """
    The total amount of commission paid for this instrument over the lifetime of the Account.
    """
    guaranteed_execution_fees: Annotated[Optional[AccountUnits], TransportField(None, alias="guaranteedExecutionFees")]
    """
    The total amount of fees charged over the lifetime of the Account for the execution of guaranteed Stop Loss Orders for this instrument.
    """
    long: Annotated[Optional[PositionSide], TransportField(None)]
    """
    The details of the long side of the Position.
    """
    short: Annotated[Optional[PositionSide], TransportField(None)]
    """
    The details of the short side of the Position.
    """


__all__ = ("Position",)
