
"""model definition for OANDA v20 REST API (3.0.25)"""




from typing import Optional



from ..transport import ApiObject, TransportField
from ..util import exporting



class ConfigureAccountRequest(ApiObject):
    """
    ConfigureAccountRequest
    """
    alias: Optional[str] = TransportField(None)
    """Client-defined alias (name) for the Account
    """
    margin_rate: Optional[str] = TransportField(None, alias="marginRate")
    """The string representation of a decimal number.
    """


__all__ = exporting(__name__, ...)

