"""TradeSummary model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .common_types import TradeId, InstrumentName, PriceValue, Time, LotsValue, AccountUnits, TransactionId, OrderId
from .trade_state import TradeState
from .client_extensions import ClientExtensions


class TradeSummary(ApiObject):
    """
    The summary of a Trade within an Account. This representation does not provide the full details of the Trade's dependent Orders.
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

    open_time: Annotated[Time, TransportField(..., alias="openTime")]
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

    close_time: Annotated[Optional[Time], TransportField(None, alias="closeTime")]
    """
    The date/time when the Trade was fully closed. Only provided for Trades whose state is CLOSED.
    """

    client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="clientExtensions")]
    """
    The client extensions of the Trade.
    """

    take_profit_order_id: Annotated[Optional[OrderId], TransportField(None, alias="takeProfitOrderID")]
    """
    ID of the Trade's Take Profit Order, only provided if such an Order exists.
    """

    stop_loss_order_id: Annotated[Optional[OrderId], TransportField(None, alias="stopLossOrderID")]
    """
    ID of the Trade's Stop Loss Order, only provided if such an Order exists.
    """

    guaranteed_stop_loss_order_id: Annotated[Optional[OrderId], TransportField(None, alias="guaranteedStopLossOrderID ")]
    """
    ID of the Trade's Guaranteed Stop Loss Order, only provided if such an Order exists.

    supplemental to v20 3.0.25
    """

    trailing_stop_loss_order_id: Annotated[Optional[OrderId], TransportField(None, alias="trailingStopLossOrderID")]
    """
    ID of the Trade's Trailing Stop Loss Order, only provided if such an Order exists.
    """


__all__ = ("TradeSummary",)
