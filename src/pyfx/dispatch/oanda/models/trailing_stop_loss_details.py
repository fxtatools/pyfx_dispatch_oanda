"""TrailingStopLossDetails model definition for OANDA v20 REST API (3.0.25)"""

from .trade_dependent_mixins import TradeDependentDetails


class TrailingStopLossDetails(TradeDependentDetails):
    """TrailingStopLossDetails specifies the details of a Trailing Stop Loss Order to be created on behalf of a client.

    This may happen when an Order is filled that opens a Trade requiring a Trailing Stop Loss, or when a Trade's
    dependent Trailing Stop Loss Order is modified directly through the Trade.
    """


__all__ = ("TrailingStopLossDetails",)
