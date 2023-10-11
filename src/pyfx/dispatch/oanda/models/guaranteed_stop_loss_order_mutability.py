from enum import Enum


class GuaranteedStopLossOrderMutability(str, Enum):
    """For Accounts that support guaranteed Stop Loss Orders, describes the actions that can be be performed on guaranteed Stop Loss Orders.

    Supplemental to v20 3.0.25
    """

    Fixed = "FIXED"  # Once a guaranteed Stop Loss Order has been created it cannot be replaced or cancelled.
    Replaceable = "REPLACEABLE"  # An existing guaranteed Stop Loss Order can only be replaced, not cancelled.
    Cancellable = "CANCELABLE"  # Once a guaranteed Stop Loss Order has been created it can be either replaced or cancelled.
    PriceWidenOnly = "PRICE_WIDEN_ONLY"  # An existing guaranteed Stop Loss Order can only be replaced to widen the gap from the current price, not cancelled"

__all__ = ("GuaranteedStopLossOrderMutability",)
