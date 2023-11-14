"""FundingReason definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class FundingReason(ApiEnum):
    """
    The reason that an Account is being funded.
    """


    __finalize__: ClassVar[Literal[True]] = True

    CLIENT_FUNDING = 'CLIENT_FUNDING'
    ACCOUNT_TRANSFER = 'ACCOUNT_TRANSFER'
    DIVISION_MIGRATION = 'DIVISION_MIGRATION'
    SITE_MIGRATION = 'SITE_MIGRATION'
    ADJUSTMENT = 'ADJUSTMENT'


__all__ = ("FundingReason",)
