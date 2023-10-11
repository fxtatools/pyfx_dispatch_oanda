
"""model definition for OANDA v20 REST API (3.0.25)"""

from pandas import Timestamp
from typing import Optional

from .price_bucket import PriceBucket


from ..transport import ApiObject, TransportField
from ..util import exporting


class Price(ApiObject):
    """
    The Price representation
    """
    instrument: Optional[str] = TransportField(None)
    """
    The Price's Instrument.
    """
    tradeable: Optional[bool] = TransportField(None)
    """
    Flag indicating if the Price is tradeable or not
    """
    timestamp: Optional[Timestamp] = TransportField(None)
    """
    The date/time when the Price was created.
    """
    base_bid: Optional[str] = TransportField(None, alias="baseBid")
    """
    The base bid price as calculated by pricing.
    """
    base_ask: Optional[str] = TransportField(None, alias="baseAsk")
    """
    The base ask price as calculated by pricing.
    """
    bids: Optional[list[PriceBucket]] = TransportField(None)
    """
    The list of prices and liquidity available on the Instrument's bid side. It is possible for this list to be empty if there is no bid liquidity currently available for the Instrument in the Account.
    """
    asks: Optional[list[PriceBucket]] = TransportField(None)
    """
    The list of prices and liquidity available on the Instrument's ask side. It is possible for this list to be empty if there is no ask liquidity currently available for the Instrument in the Account.
    """
    closeout_bid: Optional[str] = TransportField(None, alias="closeoutBid")
    """
    The closeout bid price. This price is used when a bid is required to closeout a Position (margin closeout or manual) yet there is no bid liquidity. The closeout bid is never used to open a new position.
    """
    closeout_ask: Optional[str] = TransportField(None, alias="closeoutAsk")
    """
    The closeout ask price. This price is used when an ask is required to closeout a Position (margin closeout or manual) yet there is no ask liquidity. The closeout ask is never used to open a new position.
    """


__all__ = exporting(__name__, ...)
