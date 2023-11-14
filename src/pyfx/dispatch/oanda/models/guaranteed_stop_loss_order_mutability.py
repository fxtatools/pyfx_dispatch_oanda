from typing import Literal
from typing_extensions import ClassVar

from .api_enum import ApiEnum


class GuaranteedStopLossOrderMutability(ApiEnum):
    """For Accounts that support guaranteed Stop Loss Orders, describes the actions that can be be performed on guaranteed Stop Loss Orders.

    Supplemental to v20 3.0.25
    """

    __finalize__: ClassVar[Literal[True]] = True

    FIXED = "FIXED"  # Once a guaranteed Stop Loss Order has been created it cannot be replaced or cancelled.
    REPLACEABLE = "REPLACEABLE"  # An existing guaranteed Stop Loss Order can only be replaced, not cancelled.
    CANCELABLE = "CANCELABLE"  # Once a guaranteed Stop Loss Order has been created it can be either replaced or cancelled.
    PRICE_WIDEN_ONLY = "PRICE_WIDEN_ONLY"  # An existing guaranteed Stop Loss Order can only be replaced to widen the gap from the current price, not cancelled"

__all__ = ("GuaranteedStopLossOrderMutability",)
