
"""CalculatedTradeState model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .common_types import TradeId, AccountUnits


class CalculatedTradeState(ApiObject):
    """
    The dynamic (calculated) state of an open Trade
    """

    id: Annotated[Optional[TradeId], TransportField(None)]
    """The Trade's ID.
    """

    unrealized_pl: Annotated[Optional[AccountUnits], TransportField(None, alias="unrealizedPL")]
    """The Trade's unrealized profit/loss.
    """

    margin_used: Annotated[Optional[AccountUnits], TransportField(None, alias="marginUsed")]
    """Margin currently used by the Trade.
    """


__all__ = ("CalculatedTradeState",)
