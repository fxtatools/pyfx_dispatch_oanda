
"""ClosePositionRequest model definition for OANDA v20 REST API (3.0.25)"""

from json import JSONEncoder
from typing import Annotated, Optional

from numpy import double

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .client_extensions import ClientExtensions

from ..transport.transport_types import TransportType
from .common_types import DoubleConstants


class TransportClosePositionUnits(TransportType[float, str]):
    """Transport type interface for ClosePositionRequest units"""

    @classmethod
    def parse(cls, value: str | float) -> float:
        if isinstance(value, float):
            return value
        elif value == "ALL":
            return DoubleConstants.INF.value  # type: ignore
        elif value == "NONE":
            return DoubleConstants.ZERO.value  # type: ignore
        else:
            return double(value)  # type: ignore

    @classmethod
    def unparse(cls, value: float, encoder: Optional[JSONEncoder] = None) -> str:
        if value == DoubleConstants.ZERO:
            return "NONE"
        elif value == DoubleConstants.INF:
            return "ALL"
        else:
            return str(value)


class ClosePositionRequest(ApiObject):
    """ClosePositionRequest"""

    long_units: Annotated[Optional[double], TransportField(DoubleConstants.INF, alias="longUnits", transport_type=TransportClosePositionUnits)]
    """Indication of how much of the long Position to closeout.

    Either the string \"ALL\", the string \"NONE\", or a DecimalNumber representing how many units of the long position to close using a PositionCloseout MarketOrder.

    The units specified must always be positive.
    """

    long_client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="longClientExtensions")]
    """The client extensions to add to the MarketOrder used to close the long position.
    """

    short_units: Annotated[Optional[double], TransportField(DoubleConstants.INF, alias="shortUnits", transport_type=TransportClosePositionUnits)]
    """Indication of how much of the short Position to closeout.

    Either the string \"ALL\", the string \"NONE\", or a DecimalNumber representing how many units of the short position to close using a PositionCloseout MarketOrder.

    The units specified must always be positive.
    """

    short_client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="shortClientExtensions")]
    """The client extensions to add to the MarketOrder used to close the short position.
    """


__all__ = ("ClosePositionRequest", "TransportClosePositionUnits")
