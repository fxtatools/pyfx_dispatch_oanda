
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from .client_extensions import ClientExtensions

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


class SetTradeClientExtensionsRequest(ApiObject):
    """
    SetTradeClientExtensionsRequest
    """
    client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="clientExtensions")]


__all__ = exporting(__name__, ...)
