"""MarketOrderMarginCloseoutReason definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class MarketOrderMarginCloseoutReason(ApiEnum):
    """
    The reason that the Market Order was created to perform a margin closeout
    """


    __finalize__: ClassVar[Literal[True]] = True

    MARGIN_CHECK_VIOLATION = 'MARGIN_CHECK_VIOLATION'
    REGULATORY_MARGIN_CALL_VIOLATION = 'REGULATORY_MARGIN_CALL_VIOLATION'
    REGULATORY_MARGIN_CHECK_VIOLATION = 'REGULATORY_MARGIN_CHECK_VIOLATION'


__all__ = ("MarketOrderMarginCloseoutReason",)
