"""Common mixin classes for Order classes"""

from typing import Optional
from ..util.naming import exporting

from ..transport import TransportField

from .common_types import InstrumentName, Time, OrderId, TradeId, TransactionId, LotsValue

from .order import Order
from .order_type import OrderType
from .order_trigger_condition import OrderTriggerCondition
from .client_extensions import ClientExtensions
from .guaranteed_stop_loss_details import GuaranteedStopLossDetails
from .order_position_fill import OrderPositionFill
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .time_in_force import TimeInForce
from .trailing_stop_loss_details import TrailingStopLossDetails


class OrderBase(Order):
    """
    Supplemental base class for common fields in Order class definitions

    The OrderBase class provides field definitions for common fields in effective
    subclasses of the Order class, for the fxTrade v20 API
    """

    type: OrderType = TransportField(...)
    """
    The type of the Order. Required value is unique to each order class.
    """

    time_in_force: TimeInForce = TransportField(..., alias="timeInForce")
    """
    The time-in-force requested for the Market Order. Accepted values will vary by request class
    """

    filling_transaction_id: Optional[TransactionId] = TransportField(None, alias="fillingTransactionID")
    """
    ID of the Transaction that filled this Order (only provided when the Order's state is FILLED)
    """

    filled_time: Time = TransportField(None, alias="filledTime")
    """
    Date/time when the Order was filled (only provided when the Order's state is FILLED)
    """

    trade_opened_id: Optional[TradeId] = TransportField(None, alias="tradeOpenedID")
    """
    Trade ID of Trade opened when the Order was filled (only provided when the Order's state is FILLED and a Trade was opened as a result of the fill)
    """

    trade_reduced_id: Optional[TradeId] = TransportField(None, alias="tradeReducedID")
    """
    Trade ID of Trade reduced when the Order was filled (only provided when the Order's state is FILLED and a Trade was reduced as a result of the fill)
    """

    trade_closed_ids: Optional[list[TradeId]] = TransportField(None, alias="tradeClosedIDs")
    """
    Trade IDs of Trades closed when the Order was filled (only provided when the Order's state is FILLED and one or more Trades were closed as a result of the fill)
    """

    cancelling_transaction_id: Optional[TransactionId] = TransportField(None, alias="cancellingTransactionID")
    """
    ID of the Transaction that cancelled the Order (only provided when the Order's state is CANCELLED)
    """

    cancelled_time: Time = TransportField(None, alias="cancelledTime")
    """
    Date/time when the Order was cancelled (only provided when the state of the Order is CANCELLED)
    """


class LimitOrderMixin(OrderBase):
    """
    Mixin class for limit-based orders
    """
    ## subclasses: all Order classes except FixedPriceOrder, MarketOrder

    gtd_time: Time = TransportField(None, alias="gtdTime")
    """
    The date/time when the Limit Order will be cancelled if its timeInForce is \"GTD\".
    """

    trigger_condition: Optional[OrderTriggerCondition] = TransportField(OrderTriggerCondition.DEFAULT, alias="triggerCondition")
    """
    Specification of which price component should be used when determining if an Order should be triggered and filled. This allows Orders to be triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price depending on the desired behaviour. Orders are always filled using their default price component. This feature is only provided through the REST API. Clients who choose to specify a non-default trigger condition will not see it reflected in any of OANDA's proprietary or partner trading platforms, their transaction history or their account statements. OANDA platforms always assume that an Order's trigger condition is set to the default value when indicating the distance from an Order's trigger price, and will always provide the default trigger condition when creating or modifying an Order. A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition value must either be \"DEFAULT\", or the \"natural\" trigger side \"DEFAULT\" results in. So for a Stop Loss Order for a long trade valid values are \"DEFAULT\" and \"BID\", and for short trades \"DEFAULT\" and \"ASK\" are valid.
    """


class ReplacesOrderMixin(OrderBase):
    """
    Mixin class for Order classes recording order replacement events
    """
    ## subclasses:
    ## MarketIfTouchedOrder, StopLossOrder, StopOrder, TakeProfitOrder, TrailingStopLossOrder

    replaces_order_id: Optional[OrderId] = TransportField(None, alias="replacesOrderID")
    """
    The ID of the Order that was replaced by this Order (only provided if this Order was created as part of a cancel/replace).
    """

    replaced_by_order_id: Optional[OrderId] = TransportField(None, alias="replacedByOrderID")
    """
    The ID of the Order that replaced this Order (only provided if this Order was cancelled as part of a cancel/replace).
    """


class UnitsOrderBase(OrderBase):
    """Common base class for units-focused orders"""

    ## subclasses: FixedPriceOrder, LimitOrder, MarketIfTouchedOrder, MarketOrder, StopOrder

    instrument: InstrumentName = TransportField(...)
    """
    The Fixed Price Order's Instrument.
    """

    units: LotsValue = TransportField(...)
    """
    The quantity requested to be filled by the Fixed Price Order. A posititive number of units results in a long Order, and a negative number of units results in a short Order.

    """

    position_fill: Optional[OrderPositionFill] = TransportField(OrderPositionFill.DEFAULT, alias="positionFill")
    """
    Specification of how Positions in the Account are modified when the Order is filled.
    """

    take_profit_on_fill: Optional[TakeProfitDetails] = TransportField(None, alias="takeProfitOnFill")
    """
    TakeProfitDetails specifies the details of a Take Profit Order to be
    created on behalf of a client. This may happen when an Order is filled
    that opens a Trade requiring a Take Profit, or when a Trade’s dependent
    Take Profit Order is modified directly through the Trade.
    """

    stop_loss_on_fill: Optional[StopLossDetails] = TransportField(None, alias="stopLossOnFill")
    """
    StopLossDetails specifies the details of a Stop Loss Order to be created
    on behalf of a client. This may happen when an Order is filled that opens
    a Trade requiring a Stop Loss, or when a Trade’s dependent Stop Loss
    Order is modified directly through the Trade.
    """

    guaranteed_stop_loss_on_fill: Optional[GuaranteedStopLossDetails] = TransportField(None, alias="guaranteedStopLossOnFill")
    """
    GuaranteedStopLossDetails specifies the details of a Guaranteed Stop Loss
    Order to be created on behalf of a client. This may happen when an Order
    is filled that opens a Trade requiring a Guaranteed Stop Loss, or when a
    Trade’s dependent Guaranteed Stop Loss Order is modified directly through
    the Trade.
    """

    trailing_stop_loss_on_fill: Optional[TrailingStopLossDetails] = TransportField(None, alias="trailingStopLossOnFill")
    """
    TrailingStopLossDetails specifies the details of a Trailing Stop Loss
    Order to be created on behalf of a client. This may happen when an Order
    is filled that opens a Trade requiring a Trailing Stop Loss, or when a
    Trade’s dependent Trailing Stop Loss Order is modified directly through
    the Trade.
    """

    trade_client_extensions: Optional[ClientExtensions] = TransportField(None, alias="tradeClientExtensions")
    """
    Client Extensions to add to the Trade created when the Order is filled
    (if such a Trade is created). Do not set, modify, or delete
    tradeClientExtensions if your account is associated with MT4.
    """


__all__ = tuple(exporting(__name__, ...))
