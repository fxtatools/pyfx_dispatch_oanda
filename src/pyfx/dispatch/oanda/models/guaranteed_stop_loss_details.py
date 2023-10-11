"""GuaranteedStopLossDetails model definition, supplemental to v20 3.0.25"""

from typing import Optional

from ..transport import ApiObject, TransportField
from .client_extensions import ClientExtensions
from .common_types import PriceValue, Time
from .time_in_force import TimeInForce


class GuaranteedStopLossDetails(ApiObject):

    price: Optional[PriceValue] = TransportField(None)
    """  
    The price that the Guaranteed Stop Loss Order will be triggered at. Only
    one of the price and distance fields may be specified.
    """

    distance: Optional[PriceValue] = TransportField(None)
    """
    Specifies the distance (in price units) from the Trade’s open price to
    use as the Guaranteed Stop Loss Order price. Only one of the distance and
    price fields may be specified.
    """

    time_in_force: Optional[TimeInForce] = TransportField(TimeInForce.GTC, alias="timeInForce")
    """    
    The time in force for the created Guaranteed Stop Loss Order. This may
    only be GTC, GTD or GFD.
    """

    gtd_time: Optional[Time] = TransportField(None, alias="gtdTime")
    """
    The date when the Guaranteed Stop Loss Order will be cancelled on if
    timeInForce is GTD.
    """

    client_extensions: Optional[ClientExtensions] = TransportField(None, alias="clientExtensions")
    """
    The Client Extensions to add to the Guaranteed Stop Loss Order when
    created.
    """


__all__ = ("GuaranteedStopLossDetails",)
