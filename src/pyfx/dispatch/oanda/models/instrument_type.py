"""InstrumentType definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class InstrumentType(ApiEnum):
    """
    The type of an Instrument.
    """


    __finalize__: ClassVar[Literal[True]] = True

    CURRENCY = 'CURRENCY'
    CFD = 'CFD'
    METAL = 'METAL'


__all__ = ("InstrumentType",)
