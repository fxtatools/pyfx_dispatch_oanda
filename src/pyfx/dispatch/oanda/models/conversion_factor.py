"""ConversionFactor model definition"""

from typing import Annotated, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import FloatValue


class ConversionFactor(ApiObject):
    """
    A ConversionFactor contains information used to convert an amount from an Instrument’s base or quote currency to the home currency of an Account.

    supplemental to the fxTrade v20 API 3.0.25
    """

    factor: Annotated[Optional[FloatValue], TransportField(None)]
    """
    The factor by which to multiply the amount in the given currency to
    obtain the amount in the home currency of the Account.
    """


__all__ = ("ConversionFactor",)
