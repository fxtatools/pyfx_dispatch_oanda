
"""TimeInForce definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class TimeInForce(ApiEnum):
    """
    The time-in-force of an Order. TimeInForce describes how long an Order should remain pending before being automatically cancelled by the execution system.
    """

    __finalize__: ClassVar[Literal[True]] = True

    GTC = 'GTC'
    '''"Good until Cancelled"'''
    GTD = 'GTD'
    '''"Good until Date" and will be cancelled at the provided time'''
    GFD = 'GFD'
    '''"Good For Day" and will be cancelled at 5pm New York time'''
    FOK = 'FOK'
    '''The Order must be immediately "Filled Or Killed"'''
    IOC = 'IOC'
    '''The Order must be "Immediately partially filled Or Cancelled"'''


__all__ = ("TimeInForce",)
