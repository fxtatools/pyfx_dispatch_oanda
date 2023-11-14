"""ClientPrice model definitions for OANDA v20 REST and Streaming APIs (3.0.25)"""


from typing import Annotated, Literal, Optional

from .streaming_price_base import StreamingPriceObject, StreamingPriceType

from abc import ABC
from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from .common_types import InstrumentName, Time, PriceValue
from .price_status import PriceStatus
from .price_bucket import PriceBucket
from .quote_home_conversion_factors import QuoteHomeConversionFactors
from .units_available import UnitsAvailable


class ClientPriceBase(ApiObject, ABC):
    """Common base class for Client-specific price

    ClientPriceBase provides a base class with common field
    definitions for the following implementation classes

    - StreamingPrice, as adapted for the streaming price endpoint
    - ClientPrice, as applied within OrderFillTransaction objects
    """

    instrument: Annotated[Optional[InstrumentName], TransportField(None)]
    """
    The Price's Instrument (when provided in the object)
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


class StreamingPrice(ClientPriceBase, StreamingPriceObject):

    """
    The specification of an Account-specific Price, as presented via the v20 streaming price endpoint

    This class is adapted after the definition of ClientPrice in the v20 API JSON schema, version
    3.0.25. The StreamingPrice class definition diverges to the present ClientPrice class definition,
    in the following characteristics:

    - The presence of the 'type' field, in the StreamingPrice class.
    - The name of the respective 'time' or 'timestamp' field, for each of the StreamingPrice and
      ClientPrice classes.

    StreamingPrice is implemented as a subclass of StreamingPriceObject, complimentary to the
    PricingHeartbeat class. In processing for server response messages for the streaming price
    endpoint, the two StreamingPriceObject subclasses are each differentiated by the content of
    the `type` field, whether `"PRICE"` or `"HEARTBEAT"`. The StreamingPriceType enum class provides
    an internal representation of values for this generally constant field.
    """

    type: Annotated[Literal[StreamingPriceType.PRICE], TransportField(...)] = StreamingPriceType.PRICE
    """
    The string \"PRICE\". Used to identify a Price object when found in a stream.
    """

    time: Annotated[Time, TransportField(...)]
    """
    The date/time when the Price was created
    """


class ClientPrice(ClientPriceBase):
    """
    The specification of an Account-specific Price, as presented within order fill transaction logs
    """

    timestamp: Annotated[Time, TransportField(...)]
    """
    The date/time when the Price was created
    """


__all__ = "ClientPriceBase", "StreamingPrice", "ClientPrice"
