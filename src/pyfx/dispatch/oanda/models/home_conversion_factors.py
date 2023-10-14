"""HomeConversionFactors model definition"""

from typing import Annotated, Optional

from ..transport import ApiObject, TransportField
from .conversion_factor import ConversionFactor

class HomeConversionFactors(ApiObject):
    """
    A HomeConversionFactors message contains information used to convert amounts from an Instrument’s base or quote currency to the home currency of an Account.

    supplemental to the fxTrade v20 API 3.0.25
    """

    gainQuoteHome: Optional[ConversionFactor] = TransportField(None, alias="gainQuoteHome")
    """
    The ConversionFactor in effect for the Account for converting any gains
    realized in Instrument quote units into units of the Account’s home
    currency.
    """

    loss_quote_home: Annotated[Optional[ConversionFactor], TransportField(None, alias="lossQuoteHome")]
    """
    The ConversionFactor in effect for the Account for converting any losses
    realized in Instrument quote units into units of the Account’s home
    currency.
    """

    gain_base_home: Annotated[Optional[ConversionFactor], TransportField(None, alias="gainBaseHome")]
    """
    The ConversionFactor in effect for the Account for converting any gains
    realized in Instrument base units into units of the Account’s home
    currency.
    """

    loss_base_home: Annotated[Optional[ConversionFactor], TransportField(None, alias="lossBaseHome")]
    """    
    The ConversionFactor in effect for the Account for converting any losses
    realized in Instrument base units into units of the Account’s home
    currency.
    """


__all__ = ("HomeConversionFactors",)
