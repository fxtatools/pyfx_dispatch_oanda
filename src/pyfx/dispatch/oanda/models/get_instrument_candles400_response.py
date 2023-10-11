
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional



from ..transport import ApiObject, TransportField
from ..util import exporting


class FxTrade400Response(ApiObject):
    """
    FxTrade400Response, based on GetInstrumentCandles400Response produced by OpenAPI Generator
    """
    error_code: Optional[str] = TransportField(None, alias="errorCode")
    """
    The code of the error that has occurred. This field may not be returned for some errors.
    """
    error_message: Optional[str] = TransportField(None, alias="errorMessage")
    """
    The human-readable description of the error that has occurred.
    """


__all__ = exporting(__name__, ...)
