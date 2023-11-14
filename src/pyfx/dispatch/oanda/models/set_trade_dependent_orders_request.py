"""SetTradeDependentOrdersRequest model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Mapping, Optional, Union
from typing_extensions import ClassVar

from ..transport.data import ApiObject, TransportObjectType
from ..transport.transport_fields import TransportField

from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from .guaranteed_stop_loss_details import GuaranteedStopLossDetails

from .trade_dependent_mixins import TransportTradeDependent


class SetTradeDependentOrdersRequest(ApiObject):
    """
    SetTradeDependentOrdersRequest
    """

    take_profit: Annotated[
        Optional[TakeProfitDetails],
        TransportField(None, alias="takeProfit")
    ]
    """The specification of the Take Profit to create/modify/cancel.

    If takeProfit is set to null, the Take Profit Order will be cancelled if it exists.

    If takeProfit is not provided, the existing Take Profit Order will not be modified.

    If a sub-field of takeProfit is not specified, that field will be set to a default value
    on create, and inherited by the replacing order on modify.
    """

    stop_loss: Annotated[
        Optional[StopLossDetails],
        TransportField(None, alias="stopLoss")
    ]
    """The specification of the Stop Loss to create/modify/cancel.

    If stopLoss is set to null, the Stop Loss Order will be cancelled if it exists.

    If stopLoss is not provided, the existing Stop Loss Order will not be modified.

    If a sub-field of stopLoss is not specified, that field will be set to a default value
    on create, and inherited by the replacing order on modify.
    """

    trailing_stop_loss: Annotated[
        Optional[TrailingStopLossDetails],
        TransportField(None, alias="trailingStopLoss")
    ]
    """The specification of the Trailing Stop Loss to create/modify/cancel.

    If trailingStopLoss is set to null, the Trailing Stop Loss Order will be
    cancelled if it exists.

    If trailingStopLoss is not provided, the existing Trailing Stop Loss Order
    will not be modified.

    If a sub-field of trailingStopLoss is not specified, that field will be set
    to a default value on create, and inherited by the replacing order on modify.
    """

    guaranteed_stop_loss: Annotated[
        Optional[GuaranteedStopLossDetails],
        TransportField(None, alias="guaranteedStopLoss")
    ]
    """
    The specification of the Guaranteed Stop Loss to create/modify/cancel.

    If guaranteedStopLoss is set to null, the Guaranteed Stop Loss Order will
    be cancelled if it exists.

    If guaranteedStopLoss is not provided, the existing Guaranteed Stop Loss
    Order will not be modified.

    If a sub-field of guaranteedStopLoss is not specified, that field will be
    set to a default value on create, and inherited by the replacing order on
    modify.

    supplemental to the fxTrade v20 API 3.0.25
    """


__all__ = ("SetTradeDependentOrdersRequest",)
