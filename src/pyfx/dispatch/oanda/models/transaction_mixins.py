"""Mixin classes for Transaction class definition"""

from pandas import Timestamp
from typing import Annotated, Optional

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


class InstrumentTxn(Transaction):
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


class ClientExtensionsTxn(Transaction):
    """Mixin for Transaction classes providing a `client_extensions` field"""

    client_extensions: Annotated[
        Optional[ClientExtensions],
        TransportField(None, alias="clientExtensions")
        ]
    """
    Client Extensions to add to the Order (only provided if the Order is
    being created with client extensions).
    """


class TimeInForceTxn(Transaction):
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


class OrderFillTxn(InstrumentTxn):
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


class ReplacementTxn(TimeInForceTxn):
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




class PositionEntryTxn(OrderFillTxn, ClientExtensionsTxn):
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


class RejectTxn(Transaction):
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


class PriceBoundEntryTransaction(PositionEntryTxn, TimeInForceTxn):
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


class PriceEntryTransaction(PositionEntryTxn):
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


class OrderStopsTransaction(ReplacementTxn, ClientExtensionsTxn, TradeIdMixin):
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


class OrderDistanceStopsTransaction(OrderStopsTransaction):
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


##
## Common Fields, by transaction class subset
##

# MarketIfTouchedOrderTransaction
# LimitOrderTransaction
# OrderFillTransaction
# StopOrderTransaction
# FixedPriceOrderTransaction
#         price
#         instrument
#         reason
#         units

# MarketIfTouchedOrderTransaction
# StopOrderTransaction
# LimitOrderTransaction
#         time_in_force
#         cancelling_transaction_id
#         instrument
#         trade_client_extensions
#         position_fill
#         take_profit_on_fill
#         gtd_time
#         units
#         trigger_condition
#         stop_loss_on_fill
#         replaces_order_id
#         trailing_stop_loss_on_fill

# MarketIfTouchedOrderTransaction
# StopOrderTransaction
# LimitOrderTransaction
# FixedPriceOrderTransaction
#         client_extensions
#         price
#         instrument
#         trade_client_extensions
#         position_fill
#         reason
#         take_profit_on_fill
#         units
#         stop_loss_on_fill
#         trailing_stop_loss_on_fill

# OrderFillTransaction
#         price
#         instrument
#         account_balance
#         financing
#         reason
#         units

# MarketIfTouchedOrderTransaction
# StopOrderTransaction
#         client_extensions
#         time_in_force
#         price_bound
#         price
#         cancelling_transaction_id
#         instrument
#         trade_client_extensions
#         position_fill
#         reason
#         take_profit_on_fill
#         units
#         gtd_time
#         trigger_condition
#         stop_loss_on_fill
#         replaces_order_id
#         trailing_stop_loss_on_fill

# MarketIfTouchedOrderTransaction
# StopLossOrderTransaction
# LimitOrderTransaction
# OrderFillTransaction
# StopOrderTransaction
# TakeProfitOrderTransaction
# FixedPriceOrderTransaction
#         price
#         reason

# StopLossOrderTransaction
# LimitOrderTransaction
# TakeProfitOrderTransaction
# MarketIfTouchedOrderTransaction
# StopOrderTransaction
#         time_in_force
#         cancelling_transaction_id
#         price
#         gtd_time
#         trigger_condition
#         replaces_order_id

# StopLossOrderTransaction
# LimitOrderTransaction
# TakeProfitOrderTransaction
# FixedPriceOrderTransaction
# MarketIfTouchedOrderTransaction
# StopOrderTransaction
#         price
#         client_extensions

# StopLossOrderTransaction
# TakeProfitOrderTransaction
#         price
#         trade_id
#         order_fill_transaction_id
#         client_trade_id

# StopLossOrderTransaction
#         price
#         distance

# MarketIfTouchedOrderTransaction
# StopLossOrderTransaction
# LimitOrderTransaction
# MarketOrderTransaction
# StopOrderTransaction
# TrailingStopLossOrderTransaction
# TakeProfitOrderTransaction
#         time_in_force

# StopLossOrderTransaction
# LimitOrderTransaction
# TrailingStopLossOrderTransaction
# TakeProfitOrderTransaction
# MarketIfTouchedOrderTransaction
# StopOrderTransaction
#         client_extensions
#         time_in_force
#         cancelling_transaction_id
#         reason
#         gtd_time
#         trigger_condition
#         replaces_order_id

# StopLossOrderTransaction
# TrailingStopLossOrderTransaction
# TakeProfitOrderTransaction
#         client_extensions
#         time_in_force
#         cancelling_transaction_id
#         client_trade_id
#         reason
#         trade_id
#         gtd_time
#         trigger_condition
#         replaces_order_id
#         order_fill_transaction_id

# StopLossOrderTransaction
# TrailingStopLossOrderTransaction
#         client_extensions
#         time_in_force
#         cancelling_transaction_id
#         client_trade_id
#         reason
#         trade_id
#         gtd_time
#         trigger_condition
#         distance
#         replaces_order_id
#         order_fill_transaction_id

# DelayedTradeClosureTransaction
# LimitOrderTransaction
# StopLossOrderTransaction
# OrderFillTransaction
# TrailingStopLossOrderTransaction
# FixedPriceOrderTransaction
# TakeProfitOrderTransaction
# OrderCancelTransaction
# MarketIfTouchedOrderTransaction
# StopOrderTransaction
#         reason

# StopLossOrderTransaction
# LimitOrderTransaction
# TrailingStopLossOrderTransaction
# TakeProfitOrderTransaction
# FixedPriceOrderTransaction
# MarketIfTouchedOrderTransaction
# StopOrderTransaction
#         client_extensions
#         reason

# OrderCancelTransaction
#         order_id
#         client_order_id
#         reason

# TradeClientExtensionsModifyTransaction
# StopLossOrderTransaction
# TrailingStopLossOrderTransaction
# TakeProfitOrderTransaction
#         trade_id
#         client_trade_id

# TradeClientExtensionsModifyTransaction
#         trade_id
#         client_trade_id
#         trade_client_extensions_modify

# TradeClientExtensionsModifyTransaction
# OrderClientExtensionsModifyTransaction
#         trade_client_extensions_modify

# OrderClientExtensionsModifyTransaction
#         order_id
#         client_order_id
#         trade_client_extensions_modify

# DailyFinancingTransaction
# OrderFillTransaction
#         account_balance
#         financing

# DailyFinancingTransaction
# OrderFillTransaction
# TransferFundsTransaction
#         account_balance

# OrderClientExtensionsModifyTransaction
# OrderCancelTransaction
#         order_id
#         client_order_id

##
## common fields x market order, by transaction class subset
##


# MarketIfTouchedOrderTransaction
# StopOrderTransaction
# LimitOrderTransaction
# MarketOrderTransaction
#         take_profit_on_fill
#         trade_client_extensions
#         trailing_stop_loss_on_fill
#         time_in_force
#         units
#         stop_loss_on_fill
#         position_fill
#         instrument

# OrderCancelTransaction
# TakeProfitOrderTransaction
# DelayedTradeClosureTransaction
# MarketIfTouchedOrderTransaction
# StopOrderTransaction
# MarketOrderTransaction
# TrailingStopLossOrderTransaction
# OrderFillTransaction
# LimitOrderTransaction
# FixedPriceOrderTransaction
# StopLossOrderTransaction
#         reason

# TakeProfitOrderTransaction
# MarketIfTouchedOrderTransaction
# StopOrderTransaction
# MarketOrderTransaction
# TrailingStopLossOrderTransaction
# LimitOrderTransaction
# FixedPriceOrderTransaction
# StopLossOrderTransaction
#         client_extensions
#         reason

## <<market-activated transaction>>
# MarketIfTouchedOrderTransaction
# StopOrderTransaction
# MarketOrderTransaction
# OrderFillTransaction
# LimitOrderTransaction
# FixedPriceOrderTransaction
#         units
#         reason
#         instrument

# MarketIfTouchedOrderTransaction
# StopOrderTransaction
# MarketOrderTransaction
# LimitOrderTransaction
# FixedPriceOrderTransaction
#         take_profit_on_fill
#         trade_client_extensions
#         trailing_stop_loss_on_fill
#         client_extensions
#         units
#         reason
#         stop_loss_on_fill
#         position_fill
#         instrument
