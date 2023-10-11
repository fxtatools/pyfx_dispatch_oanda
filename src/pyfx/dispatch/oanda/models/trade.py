
"""Trade definition for OANDA v20 REST API (3.0.25)"""


from pandas import Timestamp

from typing import Optional

from .client_extensions import ClientExtensions
from .stop_loss_order import StopLossOrder
from .take_profit_order import TakeProfitOrder
from .trailing_stop_loss_order import TrailingStopLossOrder

from ..transport import ApiObject, TransportField
from ..util import exporting


from .trade_state import TradeState

class Trade(ApiObject):
    """
    The specification of a Trade within an Account. This includes the full representation of the Trade's dependent Orders in addition to the IDs of those Orders.
    """
    id: Optional[str] = TransportField(None)
    """
    The Trade's identifier, unique within the Trade's Account.
    """
    instrument: Optional[str] = TransportField(None)
    """
    The Trade's Instrument.
    """
    price: Optional[str] = TransportField(None)
    """
    The execution price of the Trade.
    """
    open_time: Timestamp = TransportField(None, alias="openTime")
    """
    The date/time when the Trade was opened.
    """
    state: Optional[TradeState] = TransportField(None)
    """
    The current state of the Trade.
    """
    initial_units: Optional[str] = TransportField(None, alias="initialUnits")
    """
    The initial size of the Trade. Negative values indicate a short Trade, and positive values indicate a long Trade.
    """
    initial_margin_required: Optional[str] = TransportField(None, alias="initialMarginRequired")
    """
    The margin required at the time the Trade was created. Note, this is the 'pure' margin required, it is not the 'effective' margin used that factors in the trade risk if a GSLO is attached to the trade.
    """
    current_units: Optional[str] = TransportField(None, alias="currentUnits")
    """
    The number of units currently open for the Trade. This value is reduced to 0.0 as the Trade is closed.
    """
    realized_pl: Optional[str] = TransportField(None, alias="realizedPL")
    """
    The total profit/loss realized on the closed portion of the Trade.
    """
    unrealized_pl: Optional[str] = TransportField(None, alias="unrealizedPL")
    """
    The unrealized profit/loss on the open portion of the Trade.
    """
    margin_used: Optional[str] = TransportField(None, alias="marginUsed")
    """
    Margin currently used by the Trade.
    """
    average_close_price: Optional[str] = TransportField(None, alias="averageClosePrice")
    """
    The average closing price of the Trade. Only present if the Trade has been closed or reduced at least once.
    """
    closing_transaction_ids: Optional[list[str]] = TransportField(None, alias="closingTransactionIDs")
    """
    The IDs of the Transactions that have closed portions of this Trade.
    """
    financing: Optional[str] = TransportField(None)
    """
    The financing paid/collected for this Trade.
    """
    close_time: Timestamp = TransportField(None, alias="closeTime")
    """
    The date/time when the Trade was fully closed. Only provided for Trades whose state is CLOSED.
    """
    client_extensions: Optional[ClientExtensions] = TransportField(None, alias="clientExtensions")
    take_profit_order: Optional[TakeProfitOrder] = TransportField(None, alias="takeProfitOrder")
    stop_loss_order: Optional[StopLossOrder] = TransportField(None, alias="stopLossOrder")
    trailing_stop_loss_order: Optional[TrailingStopLossOrder] = TransportField(None, alias="trailingStopLossOrder")


__all__ = exporting(__name__, ...)

