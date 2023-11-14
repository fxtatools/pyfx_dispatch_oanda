"""Request dispatch for GetInstrumentCandles200Response"""

from datetime import datetime
from pandas import Timestamp, Period, NaT

from typing import Annotated, Iterator, Mapping, Optional, Union
from typing_extensions import ClassVar, TypeAlias

from ...util.singular_map import SingularMap
from ...transport.transport_base import TransportTimestampType

from ...api.request_base import ApiRestRequest
from ...models.get_instrument_candles200_response import GetInstrumentCandles200Response
from ...models.candlestick import Candlestick
from ...request_constants import RequestMethod
from ...transport.data import ApiClass
from ...api.param_info import path_param, query_param, ParamInfo
from ...models.candlestick_granularity import CandlestickGranularity
from ...api.price_component import PriceComponent
from ...models.weekly_alignment import WeeklyAlignment
from ...models.common_types import InstrumentName, Time


TimeBound: TypeAlias = Union[datetime, Period, str]
Hour: TypeAlias = int
Timezone: TypeAlias = str


def parse_time_from(value: TimeBound, info: ParamInfo):
    if isinstance(value, datetime):
        if __debug__:
            if datetime == NaT:
                raise AssertionError("Not a valid TimeBound",  value)
        return value
    elif isinstance(value, Period):
        return value.start_time
    elif isinstance(value, str):
        return Timestamp(value)
    else:
        raise AssertionError("Value not recognized as TimeBound", value)


def parse_time_to(value: TimeBound, info: ParamInfo):
    if isinstance(value, datetime):
        if __debug__:
            if datetime == NaT:
                raise AssertionError("Not a valid TimeBound",  value)
        return value
    elif isinstance(value, Period):
        return value.end_time
    elif isinstance(value, str):
        return Timestamp(value)
    else:
        raise AssertionError("Value not recognized as TimeBound", value)


class GetInstrumentCandlesRequest(ApiRestRequest[GetInstrumentCandles200Response, Candlestick]):

    ## similar:
    ## /v3/accounts/{accountID}/instruments/{instrument}/candles
    ## https://developer.oanda.com/rest-live-v20/pricing-ep/

    ## related:
    ## /v3/accounts/{accountID}/candles/latest
    ## - CandleSpecifiction as a request parameter type
    ## https://developer.oanda.com/rest-live-v20/pricing-ep/

    request_method: ClassVar[RequestMethod] = RequestMethod.GET
    request_path: ClassVar[str] = '/instruments/{instrument}/candles'
    response_types: Mapping[int, ApiClass] = SingularMap(200, GetInstrumentCandles200Response)

    #
    # path parameters
    #

    instrument: Annotated[InstrumentName, path_param(...)]

    #
    # query parameters
    #

    price: Annotated[Optional[PriceComponent], query_param(PriceComponent.MID)]
    granularity: Annotated[Optional[CandlestickGranularity], query_param(CandlestickGranularity.S5)]
    count: Annotated[Optional[int], query_param(500, min=1, max=5000)]
    time_from: Annotated[Optional[Time], query_param(None, parse=parse_time_from, alias="from")]
    time_to: Annotated[Optional[Time], query_param(None, parse=parse_time_to, alias="to")]

    smooth: Annotated[Optional[bool], query_param(False)]
    include_first: Annotated[Optional[bool], query_param(True, alias="includeFirst")]
    daily_alignment: Annotated[Optional[Hour], query_param(17, min=0, max=23, alias="dailyAlignment")]
    alignment_timezone: Annotated[Optional[Timezone], query_param("America/New_York", alias="alignmentTimezone")]
    weekly_alignment: Annotated[Optional[WeeklyAlignment], query_param(WeeklyAlignment.FRIDAY, alias="weeklyAlignment")]

    ## the 'units' parameter is available at a different endpoint, as units for ask/bid VWMA
    ## /v3/accounts/{accountID}/instruments/{instrument}/candles
    ## https://developer.oanda.com/rest-live-v20/pricing-ep/
    ## - may affect any indicator calculations based on the resulting quotes data
    ## - parameter is not available for any other candlestick endpoint
    ## - the units default parameter value, 1, may be assumed throughout API responses

    @classmethod
    def response_iter(cls, response: GetInstrumentCandles200Response) -> Iterator[Candlestick]:
        return response.candles


__all__ = ("GetInstrumentCandlesRequest", "TimeBound", "Hour", "Timezone")
