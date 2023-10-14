
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Annotated, Optional


from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting



class SetTradeDependentOrdersRequest(ApiObject):
    """
    SetTradeDependentOrdersRequest
    """
    take_profit: Annotated[Optional[TakeProfitDetails], TransportField(None, alias="takeProfit")]
    stop_loss: Annotated[Optional[StopLossDetails], TransportField(None, alias="stopLoss")]
    trailing_stop_loss: Annotated[Optional[TrailingStopLossDetails], TransportField(None, alias="trailingStopLoss")]


__all__ = exporting(__name__, ...)

