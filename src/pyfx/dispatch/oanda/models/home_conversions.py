
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting


class HomeConversions(ApiObject):
    """
    HomeConversions represents the factors to use to convert quantities of a given currency into the Account's home currency. The conversion factor depends on the scenario the conversion is required for.
    """
    currency: Annotated[Optional[str], TransportField(None)]
    """
    The currency to be converted into the home currency.
    """
    account_gain: Annotated[Optional[str], TransportField(None, alias="accountGain")]
    """
    The factor used to convert any gains for an Account in the specified currency into the Account's home currency. This would include positive realized P/L and positive financing amounts. Conversion is performed by multiplying the positive P/L by the conversion factor.
    """
    account_loss: Annotated[Optional[str], TransportField(None, alias="accountLoss")]
    """
    The string representation of a decimal number.
    """
    position_value: Annotated[Optional[str], TransportField(None, alias="positionValue")]
    """
    The factor used to convert a Position or Trade Value in the specified currency into the Account's home currency. Conversion is performed by multiplying the Position or Trade Value by the conversion factor.
    """


__all__ = exporting(__name__, ...)
