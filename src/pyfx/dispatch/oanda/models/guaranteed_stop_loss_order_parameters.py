"""GuaranteedStopLossOrderParameters model definition"""

from typing import Annotated, Optional

from ..transport import ApiObject, TransportField

from .guaranteed_stop_loss_order_mutability import GuaranteedStopLossOrderMutability


class GuaranteedStopLossOrderParameters(ApiObject):
    """
    The current mutability and hedging settings related to guaranteed Stop Loss orders.

    Supplemental to v20 3.0.25
    """
    
    mutability_market_open: Annotated[Optional[GuaranteedStopLossOrderMutability], TransportField(None, alias="mutabilityMarketOpen")]
    """
    The current guaranteed Stop Loss Order mutability setting of the Account when market is open.
    """
    
    mutability_market_halted: Annotated[Optional[GuaranteedStopLossOrderMutability], TransportField(None, alias="mutabilityMarketHalted")]
    """
    The current guaranteed Stop Loss Order mutability setting of the Account when market is halted.
    """


__all__ = ("GuaranteedStopLossOrderParameters",)
