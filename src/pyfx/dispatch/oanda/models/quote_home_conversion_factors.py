
"""model definition for OANDA v20 REST API (3.0.25)"""

from typing import Optional

from ..transport import ApiObject, TransportField
from ..util import exporting

class QuoteHomeConversionFactors(ApiObject):
    """
    QuoteHomeConversionFactors represents the factors that can be used used to convert quantities of a Price's Instrument's quote currency into the Account's home currency.
    
    [Deprecated. See usage in ClientPrice]
    """
    positive_units: Optional[str] = TransportField(None, alias="positiveUnits")
    """
    The factor used to convert a positive amount of the Price's Instrument's quote currency into a positive amount of the Account's home currency.  Conversion is performed by multiplying the quote units by the conversion factor.
    """
    negative_units: Optional[str] = TransportField(None, alias="negativeUnits")
    """
    The factor used to convert a negative amount of the Price's Instrument's quote currency into a negative amount of the Account's home currency.  Conversion is performed by multiplying the quote units by the conversion factor.
    """


__all__ = exporting(__name__, ...)
