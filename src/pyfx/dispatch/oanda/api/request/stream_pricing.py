"""Request dispatch for streaming price support"""

from collections.abc import Mapping
from typing import Annotated, Optional, Sequence
from typing_extensions import ClassVar
from ...api.param_info import path_param, query_param

from ...api.request_base import ApiStreamRequest
from ...models.common_types import AccountId, InstrumentName
from ...models.streaming_price_bind import StreamingPriceObject
from ...request_constants import RequestMethod
from ...transport.data import ApiClass
from ...util.singular_map import SingularMap


class StreamPricingRequest(ApiStreamRequest[StreamingPriceObject]):
    """
    Request class for the v20 API streaming price endpoint

    StreamPricingRequest provides an API request interface for
    v20 API streaming price endpoints.

    For a StreamPricingRequest, the `response_queue` will provide
    objects of type StreamingPrice and PricingHeartbeat - generally,
    the implementation classes for the StreamingPriceObject abstract
    class.

    - Each StreamingPrice object will provide information about 'ask'
      and 'bid' prices for the object's market instrument. Furthermore,
      the StreamingPrice object indicate whether the instrument is
      tradeable, at the time of the server response message.

    - Each PricingHeartbeat will provide a server timestamp for the
      response message. Heartbeat messages will be transmitted at
      an interval of approximately five seconds.

    Account Parameters

    - `account_id`: AccountId for the request. For requests initialized
      with a request builder,  a default value for this field would be
      provided automatically, using the active Configuration instance
      under the controller for the request

    Query Parameters

    - `instruments`: Sequence of InstrumentName or instrument name
      string values

    - `snapshot`: If true (default), the response stream will provide
      an initial snapshot of prices for each requested instrument.

    - `include_home_conversions`: Include `homeConversions` information
      for instrument pricing


    Implementation Notes

    In the original v20 API JSON schema 3.0.25 and at the OANDA
    Developer Hub, the response message type for the streaming
    price endpoint is denoted generally with the class
    StreamPricing200Response.

    The StreamPricing200Response class provides a central
    representation of message types provided by a streaming
    price endpoint.

    With the following implementation, the respective message types
    for StreamPricing200Response are each implemented as a subclass
    of the abstract message class, StreamingPriceObject. The latter
    class denotes the primary response type for this request class.
    """

    request_method: ClassVar[RequestMethod] = RequestMethod.GET
    request_path: ClassVar[str] = '/accounts/{accountID}/pricing/stream'

    response_types: ClassVar[Mapping[int, ApiClass]] = SingularMap(200, StreamingPriceObject)

    ## path parameters
    account_id: Annotated[AccountId, path_param(..., alias="accountID")]
    ## query parameters
    instruments: Annotated[Sequence[InstrumentName], query_param(...)]
    snapshot: Annotated[Optional[bool], query_param(True)]
    include_home_conversions: Annotated[Optional[bool], query_param(False, alias="includeHomeConversions")]


__all__ = ("StreamPricingRequest",)
