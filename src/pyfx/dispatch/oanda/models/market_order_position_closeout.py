"""MarketOrderPositionCloseout model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import FloatValue
from .transport_types import TransportDecmialAll

class MarketOrderPositionCloseout(ApiObject):
    """
    A MarketOrderPositionCloseout specifies the extensions to a Market Order when it has been created
    to closeout a specific Position.
    """

    instrument: Annotated[Optional[str], TransportField(None)]
    """
    The instrument of the Position being closed out.
    """

    units: Annotated[FloatValue, TransportField(None, transport_type=TransportDecmialAll)]
    """
    Indication of how much of the Position to close. Either \"ALL\", or a DecimalNumber reflection a partial
    close of the Trade.

    The DecimalNumber must always be positive, and represent a number that doesn't exceed the absolute size
    of the Position.
    """

__all__ = ("MarketOrderPositionCloseout",)
