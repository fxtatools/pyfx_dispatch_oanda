"""FundingReason definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class FundingReason(str, Enum):
    """
    The reason that an Account is being funded.
    """

    CLIENT_FUNDING = 'CLIENT_FUNDING'
    ACCOUNT_TRANSFER = 'ACCOUNT_TRANSFER'
    DIVISION_MIGRATION = 'DIVISION_MIGRATION'
    SITE_MIGRATION = 'SITE_MIGRATION'
    ADJUSTMENT = 'ADJUSTMENT'


__all__ = ("FundingReason",)
