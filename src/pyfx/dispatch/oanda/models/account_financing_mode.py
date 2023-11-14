"""AccountFinancingMode definition for OANDA v20 REST API (3.0.25)"""

from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class AccountFinancingMode(ApiEnum):
    """
    The financing mode of an Account
    """


    __finalize__: ClassVar[Literal[True]] = True

    NO_FINANCING = 'NO_FINANCING'
    SECOND_BY_SECOND = 'SECOND_BY_SECOND'
    DAILY = 'DAILY'


__all__ = ("AccountFinancingMode",)
