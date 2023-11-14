
"""ClosePositionRequest model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from numpy import double

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .transport_types import TransportDecimalAllNone
from .client_extensions import ClientExtensions

from .common_types import DoubleConstants


class ClosePositionRequest(ApiObject):
    """ClosePositionRequest"""

    long_units: Annotated[Optional[double], TransportField(DoubleConstants.INF, alias="longUnits", transport_type=TransportDecimalAllNone)]
    """Indication of how much of the long Position to closeout.

    Either the string \"ALL\", the string \"NONE\", or a DecimalNumber representing how many units of the long position to close using a PositionCloseout MarketOrder.

    The units specified must always be positive.
    """

    long_client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="longClientExtensions")]
    """The client extensions to add to the MarketOrder used to close the long position.
    """

    short_units: Annotated[Optional[double], TransportField(DoubleConstants.INF, alias="shortUnits", transport_type=TransportDecimalAllNone)]
    """Indication of how much of the short Position to closeout.

    Either the string \"ALL\", the string \"NONE\", or a DecimalNumber representing how many units of the short position to close using a PositionCloseout MarketOrder.

    The units specified must always be positive.
    """

    short_client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="shortClientExtensions")]
    """The client extensions to add to the MarketOrder used to close the short position.
    """


__all__ = ("ClosePositionRequest", )
