
"""CalculatedPositionState model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .common_types import InstrumentName

class CalculatedPositionState(ApiObject):
    """
    The dynamic (calculated) state of a Position
    """
    
    instrument: Annotated[InstrumentName, TransportField(...)]
    """
    The Position's Instrument.
    """

__all__ = ("CalculatedPositionState",)
