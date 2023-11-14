
"""FixedPriceOrderReason definition for OANDA v20 REST API (3.0.25)"""


from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class FixedPriceOrderReason(ApiEnum):
    """
    The reason that the Fixed Price Order was created
    """


    __finalize__: ClassVar[Literal[True]] = True

    PLATFORM_ACCOUNT_MIGRATION = 'PLATFORM_ACCOUNT_MIGRATION'


__all__ = ("FixedPriceOrderReason",)
