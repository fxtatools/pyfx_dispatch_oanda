"""Price model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .price_bucket import PriceBucket

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField

from .common_types import InstrumentName, Time, PriceValue


class Price(ApiObject):
    """
    The Price representation

    [**Deprecated**]

    This class was produced from definitions in the fxTrade v20 API 3.0.25,
    and may not be applicable for any active fxTrade endpoints, at this time.

    See alternately: ClientPrice
    """

    instrument: Annotated[InstrumentName, TransportField(...)]
    """
    The Price's Instrument.
    """

    tradeable: Annotated[Optional[bool], TransportField(None)]
    """
    Flag indicating if the Price is tradeable or not
    """

    time: Annotated[Optional[Time], TransportField(None)]
    """
    The date/time when the Price was created.
    """

    base_bid: Annotated[Optional[PriceValue], TransportField(None, alias="baseBid")]
    """
    The base bid price as calculated by pricing.
    """

    base_ask: Annotated[Optional[PriceValue], TransportField(None, alias="baseAsk")]
    """
    The base ask price as calculated by pricing.
    """

    bids: Annotated[Optional[list[PriceBucket]], TransportField(None)]
    """
    The list of prices and liquidity available on the Instrument's bid side. It is possible for this list to be empty if there is no bid liquidity currently available for the Instrument in the Account.
    """

    asks: Annotated[Optional[list[PriceBucket]], TransportField(None)]
    """
    The list of prices and liquidity available on the Instrument's ask side. It is possible for this list to be empty if there is no ask liquidity currently available for the Instrument in the Account.
    """

    closeout_bid: Annotated[Optional[PriceValue], TransportField(None, alias="closeoutBid")]
    """
    The closeout bid price. This price is used when a bid is required to closeout a Position (margin closeout or manual) yet there is no bid liquidity. The closeout bid is never used to open a new position.
    """

    closeout_ask: Annotated[Optional[PriceValue], TransportField(None, alias="closeoutAsk")]
    """
    The closeout ask price. This price is used when an ask is required to closeout a Position (margin closeout or manual) yet there is no ask liquidity. The closeout ask is never used to open a new position.
    """


__all__ = ("Price",)
