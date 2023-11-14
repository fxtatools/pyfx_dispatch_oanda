"""TakeProfitDetails model definition for OANDA v20 REST API (3.0.25)"""

from .trade_dependent_mixins import TradeDependentPriceDetails


class TakeProfitDetails(TradeDependentPriceDetails):
    """
    TakeProfitDetails specifies the details of a Take Profit Order to be created on behalf of a client.

    This may happen when an Order is filled that opens a Trade requiring a Take Profit, or when a Trade'
    s dependent Take Profit Order is modified directly through the Trade.

    Implementation Note:

    The [v20 API documentation for TakeProfitDetails][1] does not provide a definition for a `distance` field
    in this API class. Nonetheless, a `distance` field is referenced from the documentation for the `price`
    field in the class' documentation. Moreover, the similar class StopLossDetails has been defined with a
    `distance` field.

    Consequently, a `distance` field  has been included in the definition for the TakeProfitDetails class.
    (Needs Test)

    [1]: https://developer.oanda.com/rest-live-v20/transaction-df/#TakeProfitDetails
    """


__all__ = ("TakeProfitDetails",)
