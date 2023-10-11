
"""FixedPriceOrderReason definition for OANDA v20 REST API (3.0.25)"""


from enum import Enum


class FixedPriceOrderReason(str, Enum):
    """
    The reason that the Fixed Price Order was created
    """

    PLATFORM_ACCOUNT_MIGRATION = 'PLATFORM_ACCOUNT_MIGRATION'


__all__ = ("FixedPriceOrderReason",)
