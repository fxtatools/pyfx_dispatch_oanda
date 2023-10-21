"""SetOrderClientExtensionsRequest model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .client_extensions import ClientExtensions

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField


class SetOrderClientExtensionsRequest(ApiObject):
    """
    SetOrderClientExtensionsRequest
    """

    client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="clientExtensions")]
    """The Client Extensions to update for the Order.

    Do not set, modify, or delete clientExtensions if your account is associated with MT4.
    """

    trade_client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="tradeClientExtensions")]
    """The Client Extensions to update for the Trade created when the Order is filled.

    Do not set, modify, or delete clientExtensions if your account is associated with MT4.
    """


__all__ = ("SetOrderClientExtensionsRequest",)
