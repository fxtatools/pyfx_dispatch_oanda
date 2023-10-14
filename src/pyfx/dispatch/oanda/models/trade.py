
"""Trade model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .common_types import TradeId, InstrumentName, PriceValue, Time, LotsValue, AccountUnits, TransactionId
from .client_extensions import ClientExtensions
from .stop_loss_order import StopLossOrder
from .take_profit_order import TakeProfitOrder
from .trailing_stop_loss_order import TrailingStopLossOrder
from .trade_state import TradeState


class Trade(ApiObject):
    """
    The specification of a Trade within an Account. This includes the full representation of the Trade's dependent Orders in addition to the IDs of those Orders.
    """

    id: Annotated[TradeId, TransportField(...)]
    """
    The Trade's identifier, unique within the Trade's Account.
    """

    instrument: Annotated[Optional[InstrumentName], TransportField(None)]
    """
    The Trade's Instrument.
    """

    price: Annotated[Optional[PriceValue], TransportField(None)]
    """
    The execution price of the Trade.
    """

    open_time: Annotated[Time, TransportField(None, alias="openTime")]
    """
    The date/time when the Trade was opened.
    """

    state: Annotated[Optional[TradeState], TransportField(None)]
    """
    The current state of the Trade.
    """

    initial_units: Annotated[Optional[LotsValue], TransportField(None, alias="initialUnits")]
    """
    The initial size of the Trade. Negative values indicate a short Trade, and positive values indicate a long Trade.
    """

    initial_margin_required: Annotated[Optional[AccountUnits], TransportField(None, alias="initialMarginRequired")]
    """
    The margin required at the time the Trade was created. Note, this is the 'pure' margin required, it is not the 'effective' margin used that factors in the trade risk if a GSLO is attached to the trade.
    """

    current_units: Annotated[Optional[LotsValue], TransportField(None, alias="currentUnits")]
    """
    The number of units currently open for the Trade. This value is reduced to 0.0 as the Trade is closed.
    """

    realized_pl: Annotated[Optional[AccountUnits], TransportField(None, alias="realizedPL")]
    """
    The total profit/loss realized on the closed portion of the Trade.
    """

    unrealized_pl: Annotated[Optional[AccountUnits], TransportField(None, alias="unrealizedPL")]
    """
    The unrealized profit/loss on the open portion of the Trade.
    """

    margin_used: Annotated[Optional[AccountUnits], TransportField(None, alias="marginUsed")]
    """
    Margin currently used by the Trade.
    """

    average_close_price: Annotated[Optional[PriceValue], TransportField(None, alias="averageClosePrice")]
    """
    The average closing price of the Trade. Only present if the Trade has been closed or reduced at least once.
    """

    closing_transaction_ids: Annotated[Optional[list[TransactionId]], TransportField(None, alias="closingTransactionIDs")]
    """
    The IDs of the Transactions that have closed portions of this Trade.
    """

    financing: Annotated[Optional[AccountUnits], TransportField(None)]
    """
    The financing paid/collected for this Trade.
    """

    close_time: Annotated[Time, TransportField(None, alias="closeTime")]
    """
    The date/time when the Trade was fully closed. Only provided for Trades whose state is CLOSED.
    """

    client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="clientExtensions")]
    """
    The client extensions of the Trade.
    """

    take_profit_order: Annotated[Optional[TakeProfitOrder], TransportField(None, alias="takeProfitOrder")]
    """
    Full representation of the Trade’s Take Profit Order, only provided if such an Order exists.
    """

    stop_loss_order: Annotated[Optional[StopLossOrder], TransportField(None, alias="stopLossOrder")]
    """
    Full representation of the Trade’s Stop Loss Order, only provided if such an Order exists.
    """

    trailing_stop_loss_order: Annotated[Optional[TrailingStopLossOrder], TransportField(None, alias="trailingStopLossOrder")]
    """
    Full representation of the Trade’s Trailing Stop Loss Order, only provided if such an Order exists.
    """


__all__ = ("Trade",)
