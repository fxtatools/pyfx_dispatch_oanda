"""SetTradeClientExtensionsRequest model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .client_extensions import ClientExtensions

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField


class SetTradeClientExtensionsRequest(ApiObject):
    """
    SetTradeClientExtensionsRequest
    """

    client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="clientExtensions")]
    """The Client Extensions to update the Trade with.

    Do not add, update, or delete the Client Extensions if your account is associated with MT4.
    """

__all__ = ("SetTradeClientExtensionsRequest",)
