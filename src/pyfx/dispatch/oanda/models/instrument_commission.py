
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Optional


from ..transport import ApiObject, TransportField
from ..util import exporting


class InstrumentCommission(ApiObject):
    """
    An InstrumentCommission represents an instrument-specific commission
    """
    commission: Optional[str] = TransportField(None)
    """
    The commission amount (in the Account's home currency) charged per unitsTraded of the instrument
    """
    units_traded: Optional[str] = TransportField(None, alias="unitsTraded")
    """
    The number of units traded that the commission amount is based on.
    """
    minimum_commission: Optional[str] = TransportField(None, alias="minimumCommission")
    """
    The minimum commission amount (in the Account's home currency) that is charged when an Order is filled for this instrument.
    """


__all__ = exporting(__name__, ...)
