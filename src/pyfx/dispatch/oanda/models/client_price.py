
"""ClientPrice model definition for OANDA v20 REST and Streaming APIs (3.0.25)"""

from typing import Annotated, Literal, Optional

from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import InstrumentName, Time, PriceValue
from .price_status import PriceStatus
from .price_bucket import PriceBucket
from .quote_home_conversion_factors import QuoteHomeConversionFactors
from .units_available import UnitsAvailable


class ClientPrice(ApiObject):
    """
    The specification of an Account-specific Price.
    """

    type: Annotated[Literal["PRICE"], TransportField(...)] = "PRICE"
    """
    The string \"PRICE\". Used to identify a Price object when found in a stream.
    """

    instrument: Annotated[Optional[InstrumentName], TransportField(None)]
    """
    The Price's Instrument.
    """

    time: Annotated[Time, TransportField(..., alias="timestamp")]
    """
    The date/time when the Price was created
    """

    status: Annotated[Optional[PriceStatus], TransportField(None, deprecated=True)]
    """
    The status of the Price.
    """

    tradeable: Annotated[Optional[bool], TransportField(None)]
    """
    Flag indicating if the Price is tradeable or not
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
    The closeout bid Price. This Price is used when a bid is required to closeout a Position (margin closeout or manual) yet there is no bid liquidity. The closeout bid is never used to open a new position.
    """

    closeout_ask: Annotated[Optional[PriceValue], TransportField(None, alias="closeoutAsk")]
    """
    The closeout ask Price. This Price is used when a ask is required to closeout a Position (margin closeout or manual) yet there is no ask liquidity. The closeout ask is never used to open a new position.
    """

    quote_home_conversion_factors: Annotated[Optional[QuoteHomeConversionFactors], TransportField(None, alias="quoteHomeConversionFactors", deprecated=True)]
    units_available: Annotated[Optional[UnitsAvailable], TransportField(None, alias="unitsAvailable", deprecated=True)]


__all__ = ("ClientPrice",)
