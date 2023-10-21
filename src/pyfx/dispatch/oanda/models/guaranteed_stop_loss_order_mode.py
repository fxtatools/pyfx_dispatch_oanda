"""GuaranteedStopLossOrderMode definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class GuaranteedStopLossOrderMode(str, Enum):
    """
    The overall behaviour of the Account regarding guaranteed Stop Loss Orders.

    This class is denoted by the JSON Schema Class `GuaranteedStopLossOrderModeForInstrument`,
    in the present edition of the fxTrade v20 API
    """

    DISABLED = 'DISABLED'
    ALLOWED = 'ALLOWED'
    REQUIRED = 'REQUIRED'


__all__ = ("GuaranteedStopLossOrderMode",)
