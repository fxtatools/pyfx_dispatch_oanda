"""TransactionFilter definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class TransactionFilter(ApiEnum):
    """
    A filter that can be used when fetching Transactions
    """


    __finalize__: ClassVar[Literal[True]] = True

    ORDER = 'ORDER'
    FUNDING = 'FUNDING'
    ADMIN = 'ADMIN'
    CREATE = 'CREATE'
    CLOSE = 'CLOSE'
    REOPEN = 'REOPEN'
    CLIENT_CONFIGURE = 'CLIENT_CONFIGURE'
    CLIENT_CONFIGURE_REJECT = 'CLIENT_CONFIGURE_REJECT'
    TRANSFER_FUNDS = 'TRANSFER_FUNDS'
    TRANSFER_FUNDS_REJECT = 'TRANSFER_FUNDS_REJECT'
    MARKET_ORDER = 'MARKET_ORDER'
    MARKET_ORDER_REJECT = 'MARKET_ORDER_REJECT'
    LIMIT_ORDER = 'LIMIT_ORDER'
    LIMIT_ORDER_REJECT = 'LIMIT_ORDER_REJECT'
    STOP_ORDER = 'STOP_ORDER'
    STOP_ORDER_REJECT = 'STOP_ORDER_REJECT'
    MARKET_IF_TOUCHED_ORDER = 'MARKET_IF_TOUCHED_ORDER'
    MARKET_IF_TOUCHED_ORDER_REJECT = 'MARKET_IF_TOUCHED_ORDER_REJECT'
    TAKE_PROFIT_ORDER = 'TAKE_PROFIT_ORDER'
    TAKE_PROFIT_ORDER_REJECT = 'TAKE_PROFIT_ORDER_REJECT'
    STOP_LOSS_ORDER = 'STOP_LOSS_ORDER'
    STOP_LOSS_ORDER_REJECT = 'STOP_LOSS_ORDER_REJECT'
    TRAILING_STOP_LOSS_ORDER = 'TRAILING_STOP_LOSS_ORDER'
    TRAILING_STOP_LOSS_ORDER_REJECT = 'TRAILING_STOP_LOSS_ORDER_REJECT'
    ONE_CANCELS_ALL_ORDER = 'ONE_CANCELS_ALL_ORDER'
    ONE_CANCELS_ALL_ORDER_REJECT = 'ONE_CANCELS_ALL_ORDER_REJECT'
    ONE_CANCELS_ALL_ORDER_TRIGGERED = 'ONE_CANCELS_ALL_ORDER_TRIGGERED'
    ORDER_FILL = 'ORDER_FILL'
    ORDER_CANCEL = 'ORDER_CANCEL'
    ORDER_CANCEL_REJECT = 'ORDER_CANCEL_REJECT'
    ORDER_CLIENT_EXTENSIONS_MODIFY = 'ORDER_CLIENT_EXTENSIONS_MODIFY'
    ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT = 'ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT'
    TRADE_CLIENT_EXTENSIONS_MODIFY = 'TRADE_CLIENT_EXTENSIONS_MODIFY'
    TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT = 'TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT'
    MARGIN_CALL_ENTER = 'MARGIN_CALL_ENTER'
    MARGIN_CALL_EXTEND = 'MARGIN_CALL_EXTEND'
    MARGIN_CALL_EXIT = 'MARGIN_CALL_EXIT'
    DELAYED_TRADE_CLOSURE = 'DELAYED_TRADE_CLOSURE'
    DAILY_FINANCING = 'DAILY_FINANCING'
    RESET_RESETTABLE_PL = 'RESET_RESETTABLE_PL'


__all__ = ("TransactionFilter",)
