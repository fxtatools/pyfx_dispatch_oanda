"""TakeProfitDetails model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport import ApiObject, TransportField
from .common_types import PriceValue, Time
from .time_in_force import TimeInForce
from .client_extensions import ClientExtensions


class TakeProfitDetails(ApiObject):
    """
    TakeProfitDetails specifies the details of a Take Profit Order to be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring a Take Profit, or when a Trade's dependent Take Profit Order is modified directly through the Trade.
    """

    price: Optional[PriceValue] = TransportField(None)
    """
    The price that the Take Profit Order will be triggered at. Only one of the price and distance fields may be specified.
    """

    time_in_force: Optional[TimeInForce] = TransportField(TimeInForce.GTC, alias="timeInForce")
    """
    The time in force for the created Take Profit Order. This may only be GTC, GTD or GFD.
    """

    gtd_time: Time = TransportField(None, alias="gtdTime")
    """
    The date when the Take Profit Order will be cancelled on if timeInForce is GTD.
    """

    client_extensions: Optional[ClientExtensions] = TransportField(None, alias="clientExtensions")


__all__ = ("TakeProfitDetails",)
