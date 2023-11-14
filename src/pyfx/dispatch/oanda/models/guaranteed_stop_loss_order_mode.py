"""GuaranteedStopLossOrderMode definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class GuaranteedStopLossOrderMode(ApiEnum):
    """
    The overall behaviour of the Account regarding guaranteed Stop Loss Orders.

    This class is denoted by the JSON Schema Class `GuaranteedStopLossOrderModeForInstrument`,
    in the present edition of the fxTrade v20 API
    """

    __finalize__: ClassVar[Literal[True]] = True

    DISABLED = 'DISABLED'
    ALLOWED = 'ALLOWED'
    REQUIRED = 'REQUIRED'


__all__ = ("GuaranteedStopLossOrderMode",)
