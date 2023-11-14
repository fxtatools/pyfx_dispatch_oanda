"""Mixin classes for Transaction class definitions"""

from abc import ABC
from pandas import Timestamp
from typing import Annotated, Optional

from ..util.naming import exporting

from ..transport.transport_fields import TransportField

from .common_types import InstrumentName, PriceValue, LotsValue, OrderId, TransactionId
from .trade_id_mixin import TradeIdMixin

from .transaction import Transaction
from .client_extensions import ClientExtensions
from .order_position_fill import OrderPositionFill
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from .transaction_reject_reason import TransactionRejectReason
from .order_trigger_condition import OrderTriggerCondition
from .time_in_force import TimeInForce
from .market_order_reason import MarketOrderReason


class InstrumentTxn(Transaction, ABC):
    """Mixin for Transaction classes denoting a measure of units for an instrument"""

    instrument: Annotated[InstrumentName, TransportField(...)]
    """
    The Order's Instrument.
    """

    units: Annotated[LotsValue, TransportField(...)]
    """
    The quantity requested to be filled by the Order. A posititive number of units results in a long Order, and a negative number of units results in a short Order.
    """


# class ReasonTxn(Transaction):
#     """Mixin for Transaction classes providing a `reason` field"""

#     reason: Annotated[Optional[MarketOrderReason], TransportField(None)]
#     """
#     The reason that the order was created
#     """


class ClientExtensionsTxn(Transaction, ABC):
    """Mixin for Transaction classes providing a `client_extensions` field"""

    client_extensions: Annotated[
        Optional[ClientExtensions],
        TransportField(None, alias="clientExtensions")
    ]
    """
    Client Extensions to add to the Order (only provided if the Order is
    being created with client extensions).
    """


class TimeInForceTxn(Transaction, ABC):
    """
    Mixin for Transaction classes providing a `time_in_force` field
    """

    time_in_force: Annotated[
        TimeInForce,
        TransportField(..., alias="timeInForce")
    ]
    """
    The time-in-force requested for the Order.

    Accepted values and the parameter default value will vary by Order kind.
    """


class OrderFillTxn(InstrumentTxn, ABC):
    """
    Mixin for Transaction classes providing order fill information.
    """

    position_fill: Annotated[
        OrderPositionFill,
        TransportField(OrderPositionFill.DEFAULT, alias="positionFill")
    ]
    """
    Specification of how Positions in the Account are modified when the Order is filled.
    """

    take_profit_on_fill: Annotated[
        Optional[TakeProfitDetails],
        TransportField(None, alias="takeProfitOnFill")
    ]
    """
    The specification of the Take Profit Order that should be created for a
    Trade opened when the Order is filled (if such a Trade is created).
    """

    stop_loss_on_fill: Annotated[
        Optional[StopLossDetails],
        TransportField(None, alias="stopLossOnFill")
    ]
    """
    The specification of the Stop Loss Order that should be created for a
    Trade opened when the Order is filled (if such a Trade is created).
    """

    trailing_stop_loss_on_fill: Annotated[
        Optional[TrailingStopLossDetails],
        TransportField(None, alias="trailingStopLossOnFill")
    ]
    """
    The specification of the Trailing Stop Loss Order that should be created
    for a Trade that is opened when the Order is filled (if such a Trade is
    created).
    """

    trade_client_extensions: Annotated[
        Optional[ClientExtensions],
        TransportField(None, alias="tradeClientExtensions")
    ]
    """
    Client Extensions to add to the Trade created when the Order is filled
    (if such a Trade is created).  Do not set, modify, delete
    tradeClientExtensions if your account is associated with MT4.
    """


class ReplacementTxn(TimeInForceTxn, ABC):
    """
    Mixin for Transaction classes pertaining to order replacement
    """
    ## ^ also gtd_time, trigger_condition, time_in_force fields
    ##
    ## Effective subclasses:
    ##
    ## - LimitOrderTransaction
    ## - MarketIfTouchedOrderTransaction
    ## - StopLossOrderTransaction
    ## - StopOrderTransaction
    ## - TakeProfitOrderTransaction
    ## - TrailingStopLossOrderTransaction
    ## - Subsequently, GuaranteedStopLossOrderTransaction
    ##

    gtd_time: Annotated[Optional[Timestamp], TransportField(None, alias="gtdTime")]
    """
    The date/time when the Order will be cancelled if its timeInForce is \"GTD\".
    """

    trigger_condition: Annotated[
        OrderTriggerCondition,
        TransportField(OrderTriggerCondition.DEFAULT, alias="triggerCondition")
    ]
    """
    Specification of which price component should be used when determining if an Order should be triggered and filled.

    This allows Orders to be triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell,
    bid for buy) price depending on the desired behaviour. Orders are always filled using their default price component.

    This feature is only provided through the REST API.

    Clients who choose to specify a non-default trigger condition will not see it reflected in any of OANDA's proprietary or
    partner trading platforms, their transaction history or their account statements.

    OANDA platforms always assume that an Order's trigger condition is set to the default value when indicating the distance
    from an Order's trigger price, and will always provide the default trigger condition when creating or modifying an Order.

    A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition value must
    either be \"DEFAULT\", or the \"natural\" trigger side \"DEFAULT\" results in. So for a Stop Loss Order for a long trade,
    valid values are \"DEFAULT\" and \"BID\", and for short trades \"DEFAULT\" and \"ASK\" are valid.
    """

    replaces_order_id: Annotated[
        Optional[OrderId],
        TransportField(None, alias="replacesOrderID")
    ]
    """
    The ID of the Order that this Order replaces (only provided if this Order replaces an existing Order).
    """

    cancelling_transaction_id: Annotated[
        Optional[TransactionId],
        TransportField(None, alias="cancellingTransactionID")
    ]
    """
    The ID of the Transaction that cancels the replaced Order (only provided if this Order replaces an existing Order).
    """


class PositionEntryTxn(OrderFillTxn, ClientExtensionsTxn, ABC):
    """
    Mixin for transaction classes representing an immediate or scheduled order entry to the market
    """

    ## Effective subclasses:
    #
    # StopOrderTransaction (via PriceBoundEntryTransaction)
    # MarketIfTouchedOrderTransaction (via PriceBoundEntryTransaction)
    # MarketOrderTransaction (via PriceBoundEntryTransaction)
    # LimitOrderTransaction (via PriceEntryTransaction)
    # FixedPriceOrderTransaction (via PriceEntryTransaction)
    pass


class RejectTxn(Transaction, ABC):
    """
    Mixin class for transactions specifying a reject_reason field
    """

    reject_reason: Annotated[
        Optional[TransactionRejectReason],
        TransportField(None, alias="rejectReason")
    ]
    """
    The reason that the Reject Transaction was created
    """


class PriceBoundEntryTransaction(PositionEntryTxn, TimeInForceTxn, ABC):
    """
    Common base class for transaction classes in the following subset:
    - MarketIfTouchedOrderTransaction
    - MarketOrderTransaction
    - StopOrderTransaction
    """

    price_bound: Annotated[
        Optional[PriceValue],
        TransportField(None, alias="priceBound")
    ]
    """
    The worst price that the client is willing to have the Order filled at.
    """


class PriceEntryTransaction(PositionEntryTxn, ABC):
    """
    Common base class for transaction classes in the following subset:
    - LimitOrderTransaction
    - FixedPriceOrderTransaction
    """

    price: Annotated[PriceValue, TransportField(...)]
    """
    The price value for the Order.

    The application of this value will vary by implementing class.
    """


class OrderStopsTransaction(ReplacementTxn, ClientExtensionsTxn, TradeIdMixin, ABC):
    """
    Common base class for transactions classes representing a stops adjustment to an open positio

    This class provides a direct base class for TakeProfitOrderTransaction, as well as an effective base class for the following classes, via OrderDistanceStopsTransaction.
    - TrailingStopLossOrderTransaction
    - StopLossOrderTransaction
    """

    order_fill_transaction_id: Annotated[
        Optional[TransactionId],
        TransportField(None, alias="orderFillTransactionID")
    ]
    """
    The ID of the OrderFill Transaction that caused this Order to be created (only provided if this Order was created automatically when another Order was filled).
    """


class OrderDistanceStopsTransaction(OrderStopsTransaction, ABC):
    """
    Common base class for order stops transactions providing a `distance` field.

    This represents the following subclasses of OrderStopsTransaction:
    - TrailingStopLossOrderTransaction
    - StopLossOrderTransaction
    """

    distance: Annotated[Optional[PriceValue], TransportField(None)]
    """
    Specifies the distance (in price units) from the Account's current price
    to use as the stop price. If the Trade is short, the
    Instrument's bid price is used, and for long Trades the ask is used.
    """

__all__ = tuple(exporting(__name__, ...))
