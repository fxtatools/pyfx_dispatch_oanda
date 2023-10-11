
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Optional


from .client_extensions import ClientExtensions

from ..transport import ApiObject, TransportField
from ..util import exporting



class ClosePositionRequest(ApiObject):
    """
    ClosePositionRequest
    """
    long_units: Optional[str] = TransportField(None, alias="longUnits")
    """Indication of how much of the long Position to closeout. Either the string \"ALL\", the string \"NONE\", or a DecimalNumber representing how many units of the long position to close using a PositionCloseout MarketOrder. The units specified must always be positive.
    """
    long_client_extensions: Optional[ClientExtensions] = TransportField(None, alias="longClientExtensions")
    short_units: Optional[str] = TransportField(None, alias="shortUnits")
    """Indication of how much of the short Position to closeout. Either the string \"ALL\", the string \"NONE\", or a DecimalNumber representing how many units of the short position to close using a PositionCloseout MarketOrder. The units specified must always be positive.
    """
    short_client_extensions: Optional[ClientExtensions] = TransportField(None, alias="shortClientExtensions")


__all__ = exporting(__name__, ...)

