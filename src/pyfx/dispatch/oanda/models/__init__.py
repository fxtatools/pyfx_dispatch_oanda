# pyfx.dispatch.oanda.models

from collections.abc import Mapping
from immutables.map import Map

import os

from ..util.paths import expand_path
from ..util.imports import gen_imports

if not os.path.exists(expand_path("__imports__.py", os.path.dirname(__file__))):
    gen_imports(__name__)

from .__imports__ import *
__all__ = __imports__.__all__


#
# Bindings for concrete implementations of abstract response model classes
#

from ..transport.data import ApiObject

from .order_type import OrderType

from .create_order_request import CreateOrderRequest


#
# CreateOrderRequest - bind implementing classes
#

ORDER_REQUEST_TYPES_MAP: Mapping[OrderType, type[ApiObject]] = Map({ # type: ignore
    OrderType.MARKET: MarketOrderRequest,
    OrderType.LIMIT: LimitOrderRequest,
    OrderType.STOP: StopOrderRequest,
    OrderType.MARKET_IF_TOUCHED: MarketIfTouchedOrderRequest,
    OrderType.TAKE_PROFIT: TakeProfitOrderRequest,
    OrderType.STOP_LOSS: StopLossOrderRequest,
    OrderType.GUARANTEED_STOP_LOSS: GuaranteedStopLossOrderRequest,
    OrderType.TRAILING_STOP_LOSS: TrailingStopLossOrderRequest
})
CreateOrderRequest.bind_types(ORDER_REQUEST_TYPES_MAP)  # type: ignore

#
# Order - bind implementing classes
#

from .order import Order

ORDER_TYPE_MAP: Mapping[OrderType, type[ApiObject]] = Map({ # type: ignore
    OrderType.MARKET: MarketOrder,
    OrderType.LIMIT: LimitOrder,
    OrderType.STOP: StopOrder,
    OrderType.MARKET_IF_TOUCHED: MarketIfTouchedOrder,
    OrderType.TAKE_PROFIT: TakeProfitOrder,
    OrderType.STOP_LOSS: StopLossOrder,
    OrderType.GUARANTEED_STOP_LOSS: GuaranteedStopLossOrder,
    OrderType.TRAILING_STOP_LOSS: TrailingStopLossOrder,
    OrderType.FIXED_PRICE: FixedPriceOrder
})
# cf. https://developer.oanda.com/rest-live-v20/order-df/#Order
"""
Mapping of supported order classes and fixed order type values,
for order placement with the fxTrade v20 API
"""

Order.bind_types(ORDER_TYPE_MAP)  # type: ignore

#
# Transaction - bind implementing classes
#

from .transaction_type import TransactionType
from .transaction import Transaction

TRANSACTION_TYPES_MAP: Mapping[TransactionType, type[ApiObject]] = Map({  # type: ignore
    TransactionType.CREATE: CreateTransaction,
    TransactionType.CLOSE: CloseTransaction,
    TransactionType.REOPEN: ReopenTransaction,
    TransactionType.CLIENT_CONFIGURE: ClientConfigureTransaction,
    TransactionType.CLIENT_CONFIGURE_REJECT: ClientConfigureRejectTransaction,
    TransactionType.GUARANTEED_STOP_LOSS_ORDER: GuaranteedStopLossOrderTransaction,
    TransactionType.GUARANTEED_STOP_LOSS_ORDER_REJECT: GuaranteedStopLossOrderRejectTransaction,
    TransactionType.TRANSFER_FUNDS: TransferFundsTransaction,
    TransactionType.TRANSFER_FUNDS_REJECT: TransferFundsRejectTransaction,
    TransactionType.MARKET_ORDER: MarketOrderTransaction,
    TransactionType.MARKET_ORDER_REJECT: MarketOrderRejectTransaction,
    TransactionType.FIXED_PRICE_ORDER: FixedPriceOrderTransaction,
    TransactionType.LIMIT_ORDER: LimitOrderTransaction,
    TransactionType.LIMIT_ORDER_REJECT: LimitOrderRejectTransaction,
    TransactionType.STOP_ORDER: StopOrderTransaction,
    TransactionType.STOP_ORDER_REJECT: StopOrderRejectTransaction,
    TransactionType.MARKET_IF_TOUCHED_ORDER: MarketIfTouchedOrderTransaction,
    TransactionType.MARKET_IF_TOUCHED_ORDER_REJECT: MarketIfTouchedOrderRejectTransaction,
    TransactionType.TAKE_PROFIT_ORDER: TakeProfitOrderTransaction,
    TransactionType.TAKE_PROFIT_ORDER_REJECT: TakeProfitOrderRejectTransaction,
    TransactionType.STOP_LOSS_ORDER: StopLossOrderTransaction,
    TransactionType.STOP_LOSS_ORDER_REJECT: StopLossOrderRejectTransaction,
    TransactionType.TRAILING_STOP_LOSS_ORDER: TrailingStopLossOrderTransaction,
    TransactionType.TRAILING_STOP_LOSS_ORDER_REJECT: TrailingStopLossOrderRejectTransaction,
    TransactionType.ORDER_FILL: OrderFillTransaction,
    TransactionType.ORDER_CANCEL: OrderCancelTransaction,
    TransactionType.ORDER_CANCEL_REJECT: OrderCancelRejectTransaction,
    TransactionType.ORDER_CLIENT_EXTENSIONS_MODIFY: OrderClientExtensionsModifyTransaction,
    TransactionType.ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT: OrderClientExtensionsModifyRejectTransaction,
    TransactionType.TRADE_CLIENT_EXTENSIONS_MODIFY: TradeClientExtensionsModifyTransaction,
    TransactionType.TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT: TradeClientExtensionsModifyRejectTransaction,
    TransactionType.MARGIN_CALL_ENTER: MarginCallEnterTransaction,
    TransactionType.MARGIN_CALL_EXTEND: MarginCallExtendTransaction,
    TransactionType.MARGIN_CALL_EXIT: MarginCallExitTransaction,
    TransactionType.DELAYED_TRADE_CLOSURE: DelayedTradeClosureTransaction,
    TransactionType.DAILY_FINANCING: DailyFinancingTransaction,
    TransactionType.RESET_RESETTABLE_PL: ResetResettablePLTransaction,
})

Transaction.bind_types(TRANSACTION_TYPES_MAP)


__all__ = tuple(__all__)  # type: ignore
