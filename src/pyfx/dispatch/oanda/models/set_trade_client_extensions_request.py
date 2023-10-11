
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from .client_extensions import ClientExtensions

from ..transport import ApiObject, TransportField
from ..util import exporting


class SetTradeClientExtensionsRequest(ApiObject):
    """
    SetTradeClientExtensionsRequest
    """
    client_extensions: Optional[ClientExtensions] = TransportField(None, alias="clientExtensions")


__all__ = exporting(__name__, ...)
