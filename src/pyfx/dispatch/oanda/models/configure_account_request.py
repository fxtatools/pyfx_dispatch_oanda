
"""ConfigureAccountRequest model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .common_types import FloatValue


class ConfigureAccountRequest(ApiObject):
    """
    ConfigureAccountRequest
    """

    alias: Annotated[Optional[str], TransportField(None)]
    """Client-defined alias (name) for the Account
    """

    margin_rate: Annotated[Optional[FloatValue], TransportField(None, alias="marginRate")]
    """The string representation of a decimal number.
    """


__all__ = ("ConfigureAccountRequest",)
