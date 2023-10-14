
"""MarketOrderTransaction model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Literal, Optional

from ..transport.transport_fields import TransportField

from .transaction_mixins import PriceBoundEntryTransaction
from .transaction_type import TransactionType
from .time_in_force import TimeInForce
from .market_order_delayed_trade_close import MarketOrderDelayedTradeClose
from .market_order_margin_closeout import MarketOrderMarginCloseout
from .market_order_position_closeout import MarketOrderPositionCloseout
from .market_order_trade_close import MarketOrderTradeClose
from .market_order_reason import MarketOrderReason

class MarketOrderTransaction(PriceBoundEntryTransaction):
    """
    A MarketOrderTransaction represents the creation of a Market Order in the user’s account. A Market Order is an Order that is filled immediately at the current market price. Market Orders can be specialized when they are created to accomplish a specific task: to close a Trade, to closeout a Position or to participate in in a Margin closeout.
    """

    type: Annotated[Literal[TransactionType.MARKET_ORDER], TransportField(TransactionType.MARKET_ORDER)] = TransactionType.MARKET_ORDER
    """
    The Type of the Transaction. Always set to \"MARKET_ORDER\" in a MarketOrderTransaction.
    """

    time_in_force: Annotated[TimeInForce, TransportField(TimeInForce.FOK, alias="timeInForce")]
    """
    The time-in-force requested for the Market Order. Restricted to FOK or IOC for a MarketOrder.
    """

    trade_close: Annotated[Optional[MarketOrderTradeClose], TransportField(None, alias="tradeClose")]
    """
    Details of the Trade requested to be closed, only provided when the
    Market Order is being used to explicitly close a Trade.
    """

    long_position_closeout: Annotated[Optional[MarketOrderPositionCloseout], TransportField(None, alias="longPositionCloseout")]
    """           
    Details of the long Position requested to be closed out, only provided
    when a Market Order is being used to explicitly closeout a long Position.
    """

    short_position_closeout: Annotated[Optional[MarketOrderPositionCloseout], TransportField(None, alias="shortPositionCloseout")]
    """    
    Details of the short Position requested to be closed out, only provided
    when a Market Order is being used to explicitly closeout a short
    Position.
    """

    margin_closeout: Annotated[Optional[MarketOrderMarginCloseout], TransportField(None, alias="marginCloseout")]
    """    
    Details of the Margin Closeout that this Market Order was created for
    """

    delayed_trade_close: Annotated[Optional[MarketOrderDelayedTradeClose], TransportField(None, alias="delayedTradeClose")]
    """    
    Details of the delayed Trade close that this Market Order was created for
    """

    reason: Annotated[MarketOrderReason, TransportField(...)]
    """
    The reason that the Market Order was created
    """


__all__ = ("MarketOrderTransaction",)
