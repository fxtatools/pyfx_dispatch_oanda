"""GuaranteedStopLossDetails model definition, supplemental to v20 3.0.25"""

from .trade_dependent_mixins import TradeDependentPriceDetails


class GuaranteedStopLossDetails(TradeDependentPriceDetails):
    """GuaranteedStopLossDetails specifies the details of a Guaranteed Stop Loss Order
    to be created on behalf of a client.

    This may happen when an Order is filled that opens a Trade requiring a Guaranteed
    Stop Loss, or when a Trade's dependent Guaranteed Stop Loss Order is modified
    directly through the Trade.

    supplemental to the v20 API version 3.0.25
    """


__all__ = ("GuaranteedStopLossDetails",)
