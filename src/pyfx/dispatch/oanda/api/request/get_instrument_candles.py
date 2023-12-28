"""Request dispatch for GetInstrumentCandles200Response"""

import click
from datetime import datetime
from pandas import Timestamp, Period, NaT

from typing import Any, Annotated, Iterator, Mapping, Optional, Union
from typing_extensions import ClassVar, TypeAlias

from ...util.singular_map import SingularMap
from ...transport.transport_base import TransportTimestampType

from ...api.request_base import ApiRestRequest, T_request_co
from ...models.get_instrument_candles200_response import GetInstrumentCandles200Response
from ...models.candlestick import Candlestick
from ...request_constants import RequestMethod
from ...transport.data import ApiClass
from ...api.param_info import path_param, query_param, ParamInfo, ParamEnum
from ...models.candlestick_granularity import CandlestickGranularity
from ...api.price_component import PriceComponent #, TransportPriceComponent
from ...models.weekly_alignment import WeeklyAlignment
from ...models.common_types import InstrumentName, Time
from ..param_info import ParamTime


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


def parse_instrument_name(value: Union[str, InstrumentName], info: ParamInfo):
    name = value.upper() if isinstance(value, str) else value
    return info.transport_type.parse(name)

def parse_price_component(value: Union[str, PriceComponent], info: ParamInfo):
    if isinstance(value, PriceComponent):
        return value
    name = value.upper()
    return  PriceComponent.get(name)


class QuotesRequest(ApiRestRequest[T_request_co, Candlestick]):
    pass
class InstrumentQuotesRequest(QuotesRequest[T_request_co]):
    pass
class GetInstrumentCandlesRequest(ApiRestRequest[GetInstrumentCandles200Response, Candlestick]):
    """Fetch candlestick quotes data for an instrument.

    The repsonse will provide quotes for open, high, low, and close rates in one or
    more series of ask, bid, and median price components for the requested instrument,
    per the request `price` param. The response will also include  a volume component
    for the instrument, within the effective duration specified in the request.
    """

    ## similar:
    ## /v3/accounts/{accountID}/instruments/{instrument}/candles
    ## https://developer.oanda.com/rest-live-v20/pricing-ep/
    ## related:
    ## /v3/accounts/{accountID}/candles/latest
    ## - CandleSpecifiction as a request parameter type
    ## https://developer.oanda.com/rest-live-v20/pricing-ep/
    command_name: ClassVar[str] = __module__.rsplit(".", maxsplit=1)[-1]

    request_method: ClassVar[RequestMethod] = RequestMethod.GET
    request_path: ClassVar[str] = '/instruments/{instrument}/candles'
    response_types: Mapping[int, ApiClass] = SingularMap(200, GetInstrumentCandles200Response)

    #
    # path parameters
    #

    instrument: Annotated[InstrumentName, path_param(..., parse=parse_instrument_name)]
    """Name of the instrument"""

    #
    # query parameters
    #

    price: Annotated[
        Optional[PriceComponent],
        query_param(
            PriceComponent.MID,
            parse=parse_price_component,
            # transport_type = ParamPriceComponent,
            ## description for fxcmd --help ...
            description="""Price components for the request.

                The price component may be specified with individual letter codes, `"A"`, `"B"`,
                or `"M"`, for "ask" or  "bid" quotes or for quotes  representing  a median of
                "ask" and "bid" quotes.

                To request more than one price component, the component may be provided as a
                concatenation of "A", "B", and "M", in any order of sequence, e.g `"AB"`, or `"ABM"`.
                """
        )]

    granularity: Annotated[Optional[CandlestickGranularity], query_param(CandlestickGranularity.S5)]
    """"Timeframe granularity for the quotes request.
    """

    count: Annotated[Optional[int], query_param(500, min=1, max=5000)]
    """Number of quotes to request.

    The fxTrade API supports a maximum value of 5000 quotes per individual request.
    """

    time_from: Annotated[Optional[ParamTime], query_param(None, parse=parse_time_from, alias="from")]
    """Start of the period for the quotes request.

    This parameter supports any value accepted as a time string for `pd.Timestamp()`
    """

    time_to: Annotated[Optional[ParamTime], query_param(None, parse=parse_time_to, alias="to")]
    """End of the period for the quotes request.

    This parameter supports any value accepted as a time string for `pd.Timestamp()`
    """

    smooth: Annotated[Optional[bool], query_param(False)]
    """If True, each open price will represent the close price of the previous quotes."""

    include_first: Annotated[Optional[bool], query_param(True, alias="includeFirst")]
    """If True, the `time_from` value will be interpreted as an inclusive bound.

    If False, the `time_from` value will be interpreted as an exclusive bound.
    """

    alignment_timezone: Annotated[Optional[Timezone], query_param("America/New_York", alias="alignmentTimezone")]
    """Timezone for `daily_alignment`"""

    daily_alignment: Annotated[Optional[Hour], query_param(17, min=0, max=23, alias="dailyAlignment")]
    """Hour of the day, within the `alignment_timezone`, for the time index in quotes having a
    daily granularity
    """

    weekly_alignment: Annotated[Optional[WeeklyAlignment], query_param(WeeklyAlignment.FRIDAY, alias="weeklyAlignment")]
    """Day of the week, for the time index in quotes having a weekly granularity"""

    ## the 'units' parameter is available at a different endpoint, as units for ask/bid VWMA
    ## /v3/accounts/{accountID}/instruments/{instrument}/candles
    ## https://developer.oanda.com/rest-live-v20/pricing-ep/
    ## - may affect any indicator calculations based on the resulting quotes data
    ## - parameter is not available for any other candlestick endpoint
    ## - the units default parameter value, 1, may be assumed throughout API responses

    @classmethod
    def response_iter(cls, response: GetInstrumentCandles200Response) -> Iterator[Candlestick]:
        return response.candles


__all__ = "GetInstrumentCandlesRequest", "TimeBound", "Hour", "Timezone"
