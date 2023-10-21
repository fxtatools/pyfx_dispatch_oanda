"""Base class definitions for request classes"""

from typing import Annotated, Optional

from ..util.naming import exporting

from ..transport import TransportField, ApiObject

from .order_type import OrderType
from .common_types import InstrumentName, PriceValue, LotsValue, Time
from .guaranteed_stop_loss_details import GuaranteedStopLossDetails
from .order_position_fill import OrderPositionFill
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from .client_extensions import ClientExtensions
from .time_in_force import TimeInForce
from .order_trigger_condition import OrderTriggerCondition
from .trade_id_mixin import TradeIdMixin


class RequestBase(ApiObject):
    """Common base class for Request classes"""

    type: Annotated[OrderType, TransportField(...)]
    """
    The type of the Order to Create. Required value is unique to each request class
    """

    time_in_force: Annotated[TimeInForce, TransportField(..., alias="timeInForce")]
    """
    The time-in-force requested for the Order. Accepted values will vary by request class
    """

    client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="clientExtensions")]
    """
    The client extensions to add to the Order. Do not set, modify, or delete
    clientExtensions if your account is associated with MT4.
    """


class InstrumentRequestBase(RequestBase):
    """Common base class for requests actuated on a market instrument"""

    instrument: Annotated[InstrumentName, TransportField(...)]
    """
    The Market Order's Instrument.
    """

    units: Annotated[LotsValue, TransportField(...)]
    """
    The quantity requested to be filled by the order. A posititive number of units results in a long Order, and a negative number of units results in a short Order.
    """

    position_fill: Annotated[OrderPositionFill, TransportField(OrderPositionFill.DEFAULT, alias="positionFill")]
    """
    Specification of how Positions in the Account are modified when the Order is filled.
    """

    take_profit_on_fill: Annotated[Optional[TakeProfitDetails], TransportField(None, alias="takeProfitOnFill")]
    """
    TakeProfitDetails specifies the details of a Take Profit Order to be
    created on behalf of a client. This may happen when an Order is filled
    that opens a Trade requiring a Take Profit, or when a Trade's dependent
    Take Profit Order is modified directly through the Trade.
    """

    stop_loss_on_fill: Annotated[Optional[StopLossDetails], TransportField(None, alias="stopLossOnFill")]
    """
    StopLossDetails specifies the details of a Stop Loss Order to be created
    on behalf of a client. This may happen when an Order is filled that opens
    a Trade requiring a Stop Loss, or when a Trade's dependent Stop Loss
    Order is modified directly through the Trade.
    """

    guaranteed_stop_loss_on_fill: Annotated[Optional[GuaranteedStopLossDetails], TransportField(None, alias="guaranteedStopLossOnFill")]
    """
    GuaranteedStopLossDetails specifies the details of a Guaranteed Stop Loss
    Order to be created on behalf of a client. This may happen when an Order
    is filled that opens a Trade requiring a Guaranteed Stop Loss, or when a
    Trade's dependent Guaranteed Stop Loss Order is modified directly through
    the Trade.
    """

    trailing_stop_loss_on_fill: Annotated[Optional[TrailingStopLossDetails], TransportField(None, alias="trailingStopLossOnFill")]
    """
    TrailingStopLossDetails specifies the details of a Trailing Stop Loss
    Order to be created on behalf of a client. This may happen when an Order
    is filled that opens a Trade requiring a Trailing Stop Loss, or when a
    Trade's dependent Trailing Stop Loss Order is modified directly through
    the Trade.
    """

    trade_client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="tradeClientExtensions")]
    """
    Client Extensions to add to the Trade created when the Order is filled
    (if such a Trade is created). Do not set, modify, or delete
    tradeClientExtensions if your account is associated with MT4.
    """


class StopsRequestBase(InstrumentRequestBase, TradeIdMixin):

    gtd_time: Annotated[Time, TransportField(TimeInForce.GTC, alias="gtdTime")]
    """
    The date/time when the order will be cancelled if its timeInForce is \"GTD\".
    """

    trigger_condition: Annotated[OrderTriggerCondition, TransportField(OrderTriggerCondition.DEFAULT, alias="triggerCondition")]
    """
    Specification of which price component should be used when determining if an Order should be triggered and filled. This allows Orders to be triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price depending on the desired behaviour. Orders are always filled using their default price component. This feature is only provided through the REST API. Clients who choose to specify a non-default trigger condition will not see it reflected in any of OANDA's proprietary or partner trading platforms, their transaction history or their account statements. OANDA platforms always assume that an Order's trigger condition is set to the default value when indicating the distance from an Order's trigger price, and will always provide the default trigger condition when creating or modifying an Order. A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition value must either be \"DEFAULT\", or the \"natural\" trigger side \"DEFAULT\" results in. So for a Stop Loss Order for a long trade valid values are \"DEFAULT\" and \"BID\", and for short trades \"DEFAULT\" and \"ASK\" are valid.
    """


class PriceBoundedRequest(InstrumentRequestBase):
    """Mixin class for instrument-based requests offering a price bound"""

    # common to subclasses of InstrumentRequestBase
    # except imitOrderRequest

    price_bound: Annotated[Optional[PriceValue], TransportField(None, alias="priceBound")]
    """
    The worst price that the client is willing to have the Market Order filled at.
    """


__all__ = tuple(exporting(__name__, ...))
