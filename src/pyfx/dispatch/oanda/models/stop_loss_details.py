
"""model definition for OANDA v20 REST API (3.0.25)"""


from pandas import Timestamp


from typing import Annotated, Optional


from .client_extensions import ClientExtensions

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


from .time_in_force import TimeInForce

from .common_types import PriceValue

class StopLossDetails(ApiObject):
    """
    StopLossDetails specifies the details of a Stop Loss Order to be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring a Stop Loss, or when a Trade's dependent Stop Loss Order is modified directly through the Trade.
    """

    price: Annotated[Optional[PriceValue], TransportField(None)]
    """
    The price that the Stop Loss Order will be triggered at. Only one of the price and distance fields may be specified.
    """

    distance: Annotated[Optional[PriceValue], TransportField(None)]
    """
    Specifies the distance (in price units) from the Trade's open price to use as the Stop Loss Order price. Only one of the distance and price fields may be specified.
    """

    time_in_force: Annotated[Optional[TimeInForce], TransportField(None, alias="timeInForce")]
    """
    The time in force for the created Stop Loss Order. This may only be GTC, GTD or GFD.
    """

    gtd_time: Annotated[Timestamp, TransportField(None, alias="gtdTime")]
    """
    The date when the Stop Loss Order will be cancelled on if timeInForce is GTD.
    """

    client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="clientExtensions")]
    guaranteed: Annotated[Optional[bool], TransportField(None)]
    """
    Flag indicating that the price for the Stop Loss Order is guaranteed. The default value depends on the GuaranteedStopLossOrderMode of the account, if it is REQUIRED, the default will be true, for DISABLED or ENABLED the default is false.
    """


__all__ = exporting(__name__, ...)
