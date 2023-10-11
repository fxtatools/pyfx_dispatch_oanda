"""AccountFinancingMode definition for OANDA v20 REST API (3.0.25)"""

from enum import Enum


class AccountFinancingMode(str, Enum):
    """
    The financing mode of an Account
    """

    NO_FINANCING = 'NO_FINANCING'
    SECOND_BY_SECOND = 'SECOND_BY_SECOND'
    DAILY = 'DAILY'


__all__ = ("AccountFinancingMode",)
