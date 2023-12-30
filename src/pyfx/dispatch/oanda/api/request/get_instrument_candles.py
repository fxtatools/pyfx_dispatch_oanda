"""Request dispatch for GetInstrumentCandles200Response"""

from abc import ABC
from collections.abc import Collection
from datetime import datetime
from itertools import chain
from click.core import Context as Context
from functools import partial
from pandas import Timestamp, Period, NaT

from typing import Annotated, Iterator, Mapping, Optional, Union
from typing_extensions import TYPE_CHECKING, Self, ClassVar, TypeAlias


from ...util.naming import exporting
from ...util.singular_map import SingularMap

from ...api.request_base import ApiRestRequest, T_request_co
from ...request_constants import RequestMethod
from ..param_info import ParamInterface, ParamValues
from ...transport.data import ApiClass
from ...models.get_instrument_candles200_response import GetInstrumentCandles200Response, GetAccountCandlesLatest200Response
from ...models.candlestick import Candlestick
from ...models.candlestick_granularity import CandlestickGranularity
from ...models.common_types import InstrumentName, FloatValue
from ...models.price_component import PriceComponent
from ...models.weekly_alignment import WeeklyAlignment
from ...transport.account_id import AccountId

from ..param_info import (
    path_param, query_param, QueryParamInfo,
    ParamTime
)


TimeBound: TypeAlias = Union[datetime, Period, str]
Hour: TypeAlias = int
Timezone: TypeAlias = str


class TimeBoundInfo(QueryParamInfo[datetime, str]):
    def parse(self, value: TimeBound, context: Optional[Context] = None) -> str:
        if isinstance(value, str):
            return Timestamp(value)
        elif isinstance(value, datetime):
            if __debug__:
                if datetime is NaT or datetime == NaT:
                    raise AssertionError("Not a valid TimeBound",  value)
            return value
        else:
            raise AssertionError("Value not recognized as TimeBound", value)


class TimeFromInfo(TimeBoundInfo):
    def parse(self, value: TimeBound, context: Optional[Context] = None) -> str:
        if isinstance(value, Period):
            return value.start_time
        else:
            return super().parse(value, context)


class TimeToInfo(TimeBoundInfo):
    def parse(self, value: TimeBound, context: Optional[Context] = None) -> str:
        if isinstance(value, Period):
            return value.end_time
        else:
            return super().parse(value, context)


class PriceComponentInfo(QueryParamInfo[PriceComponent, str]):
    def parse(self, value: Union[PriceComponent, str], context: Optional[Context] = None) -> str:
        if isinstance(value, PriceComponent):
            return value
        name = value.upper()
        return PriceComponent.get(name)


class QuotesRequest(ApiRestRequest[T_request_co, Candlestick], ABC):
    # common mixin class

    request_method: ClassVar[RequestMethod] = RequestMethod.GET

    #
    # common query parameters
    #

    smooth: Annotated[
        Optional[bool],
        query_param(
            False,
            description="""If True, each open price will represent the close price of the previous quotes tick."""
        )]

    alignment_timezone: Annotated[
        Optional[Timezone],
        query_param(
            "America/New_York", alias="alignmentTimezone",
            description="""Timezone for `daily_alignment`"""
        )]

    daily_alignment: Annotated[
        Optional[Hour],
        query_param(
            17, min=0, max=23, alias="dailyAlignment",
            description="""Hour of the day, within the `alignment_timezone`, for the time index
            of quotes having a daily granularity
            """)]

    weekly_alignment: Annotated[
        Optional[WeeklyAlignment],
        query_param(
            WeeklyAlignment.FRIDAY, alias="weeklyAlignment",
            description="""Day of the week, for the time index in quotes having a weekly granularity"""
        )]


class InstrumentQuotesRequest(QuotesRequest[GetInstrumentCandles200Response], ABC):

    response_types: ClassVar[Mapping[int, ApiClass]] = SingularMap(200, GetInstrumentCandles200Response)

    @classmethod
    def response_iter(cls, response: GetInstrumentCandles200Response) -> Iterator[Candlestick]:
        return response.candles

    #
    # additional path parameters
    #
    instrument: Annotated[
        InstrumentName,
        path_param(
            ...,
            description="""Name of the instrument"""
        )]

    #
    # additional common query parameters
    #

    granularity: Annotated[
        Optional[CandlestickGranularity],
        query_param(
            # the blank line-breaks below should ensure that Click uses
            # a literal line break, when presenting the help text.
            CandlestickGranularity.S5,
            description="""Timeframe granularity for the quotes request.

            The value may be specified in FxTrade granularity syntax.

            S<D>: <D> seconds;

            M<D>: <D> minutes;

            H<D>: <D> hours;

            D: Business Day granularity;

            W: Business Week granularity;

            M: Business Month granularity;
            """
        )]

    price: Annotated[
        Optional[PriceComponent],
        PriceComponentInfo.from_field(
            PriceComponent.MID,
            # transport_type = ParamPriceComponent,
            ## description for fxcmd --help ...
            description="""Price components for the request.

                The price component may be specified with individual letter codes, `"A"`, `"B"`,
                or `"M"`, respectively for "ask"  "bid", or "mid" (median) quote series.

                To request more than one price component, the component may be provided as a
                concatenation of "A", "B", and "M", in any order of sequence, e.g `"AB"`, or `"ABM"`.
                """
        )]

    count: Annotated[
        Optional[int],
        query_param(
            500, min=1, max=5000,
            description="""Number of quotes for the request.

            The fxTrade API supports a maximum value of 5000 quotes per individual request
            """
        )]

    time_from: Annotated[
        Optional[ParamTime],
        TimeFromInfo.from_field(
            None, alias="from",
            descripiton="""Start of the period for the quotes request.

            This parameter supports any value accepted as a time string for `pd.Timestamp()`
            """)]

    time_to: Annotated[
        Optional[ParamTime],
        TimeToInfo.from_field(
            None, alias="to",
            description="""End of the period for the quotes request.

            This parameter supports any value accepted as a time string for `pd.Timestamp()`.
            """)]

    include_first: Annotated[
        Optional[bool],
        query_param(
            True, alias="includeFirst",
            description="""If True, the `time_from` value will be interpreted as an inclusive bound.

            If False, the `time_from` value will be interpreted as an exclusive bound.
            """)]


class GetInstrumentCandlesRequest(InstrumentQuotesRequest):
    """Fetch candlestick quotes data for an instrument.

    The repsonse will provide quotes for open, high, low, and close rates in one or
    more series of ask, bid, and mid (median) price components for the requested
    instrument. The price component may be selected with the request `price` param
    (default: mid).

    The response will also include a volume component for the instrument, within the
    effective duration specified in the request.
    """

    command_label: ClassVar[str] = "get_instrument_candles"
    request_path: ClassVar[str] = '/instruments/{instrument}/candles'


#
# other quotes requests for the FxTrade API
#

# InstrumentQuotesRequest

class AccountInstrumentRequest(QuotesRequest[T_request_co], ABC):

    # additional path params
    account_id: Annotated[
        AccountId,
        path_param(
            ..., alias="accountID",
            description="""Account Identifier for the request"""
        )]

    # additional query params
    units: Annotated[
        FloatValue,
        query_param(
            1, description="""Number of units for calculating volume-weighted
            average pricing, in ask and bid quote series"""
        )]


class GetAccountInstrumentCandlesRequest(AccountInstrumentRequest[GetInstrumentCandles200Response], InstrumentQuotesRequest):
    ## /v3/accounts/{accountID}/instruments/{instrument}/candles
    ## https://developer.oanda.com/rest-live-v20/pricing-ep/
    ## - 'units' request parameter here

    command_label: ClassVar[str] = "get_account_instrument_candles"
    request_path: ClassVar[str] = "/accounts/{accountID}/instruments/{instrument}/candles"


class CandleSpec:
    __slots__ = "instrument", "granularity", "component"
    if TYPE_CHECKING:
        instrument: InstrumentName
        granularity: CandlestickGranularity
        component: PriceComponent

    @classmethod
    def default_granularity(cls, instrument: InstrumentName) -> CandlestickGranularity:
        return InstrumentQuotesRequest.model_fields["granularity"].default

    @classmethod
    def default_price_component(cls, instrument: InstrumentName, granularity: CandlestickGranularity) -> PriceComponent:
        return InstrumentQuotesRequest.model_fields["price"].default

    @classmethod
    def parse_instrument(cls, instrument:  Union[str, InstrumentName]) -> InstrumentName:
        if isinstance(instrument, InstrumentName):
            return instrument
        else:
            return InstrumentName.parse(instrument)

    @classmethod
    def parse_granularity(cls, granularity: Union[str, CandlestickGranularity]) -> CandlestickGranularity:
        if isinstance(granularity, CandlestickGranularity):
            return granularity
        else:
            return CandlestickGranularity.get(granularity.upper())

    @classmethod
    def parse_component(cls, component: Union[str, PriceComponent]) -> PriceComponent:
        if isinstance(component, PriceComponent):
            return component
        else:
            return PriceComponent.get(component.upper())

    def __init__(self,
                 instrument: Union[InstrumentName, str],
                 granularity: Union[CandlestickGranularity, str, None] = None,
                 component: Union[PriceComponent, str, None] = None
                 ):
        cls: type[Self] = self.__class__
        i = cls.parse_instrument(instrument)
        g = cls.parse_granularity(granularity) if granularity else cls.default_granularity(i)
        c = cls.parse_component(component) if component else cls.default_price_component(i, g)
        self.instrument = i
        self.granularity = g
        self.component = c

    def __repr__(self) -> str:
        attr_p = partial(hasattr, self)
        none_str = "None"
        inst = str(self.instrument) if attr_p("instrument") else none_str
        g = str(self.granularity) if attr_p("granularity") else none_str
        c = str(self.component) if attr_p("component") else none_str
        cls = self.__class__.__name__
        return "<%s [%s, %s, %s] at 0x%x>" % (cls, inst, g, c, id(self))

    def __str__(self) -> str:
        return "%s:%s:%s" % (self.instrument, self.granularity, self.component,)


class TransportCandleSpec(ParamInterface[CandleSpec, str]):
    @classmethod
    def parse_arg(cls, arg: Union[str, CandleSpec], context: Optional[Context] = None) -> CandleSpec:
        if isinstance(arg, CandleSpec):
            return arg
        else:
            inst, g, c = arg.split(":")
            if inst == "":
                raise ValueError("No instrument name in str", arg)
            else:
                return CandleSpec(inst, g, c)

    @classmethod
    def unparse_url_str(cls, value: Union[str, CandleSpec]) -> str:
        return str(value)


class TransportCandleSpecSeq(ParamValues[CandleSpec, str]):
    member_transport_type = TransportCandleSpec
    storage_class = list

    @classmethod
    def parse_member(cls, value: Union[str, CandleSpec]) -> CandleSpec:
        return TransportCandleSpec.parse_arg(value)

    @classmethod
    def parse(cls, unparsed: tuple[list[CandleSpec]]):
        #
        # generally reached as a side-effect of this application's
        # Click interface. At this point, the value may in fact
        # represent a tuple of lists of parsed CandleSpec values.
        #
        # As a workaround, this will destructure the already-parsed
        # arg value and forward the request for further handling
        # under parse_arg()
        #
        return chain.from_iterable(map(cls.parse_arg, unparsed))

    @classmethod
    def parse_arg(cls, value: Union[str, Collection[Union[str, CandleSpec]]],
                  context: Optional[Context] = None) -> list[CandleSpec]:
        if isinstance(value, str):
            return [cls.parse_member(s) for s in value.split(",")]
        else:
            if __debug__:
                if not isinstance(value, Collection):
                    raise AssertionError("Unrecognized CandleSpec syntax, expected str or collection", value)
            return [cls.parse_member(elt) for elt in value]

    @classmethod
    def unparse_url_str(cls, value: Collection[Union[CandleSpec, str]]) -> str:
        if __debug__:
            if not isinstance(value, Collection):
                raise AssertionError("Not a collection", value)
        return ",".join(TransportCandleSpec.unparse_url_str(spec) for spec in value)


class GetLatestQuotesRequest(AccountInstrumentRequest[GetAccountCandlesLatest200Response]):

    command_label: ClassVar[str] = "get_latest_candles"
    request_path: ClassVar[str] = "/accounts/{accountID}/candles/latest"

    response_types: ClassVar[Mapping[int, ApiClass]] = SingularMap(200, GetAccountCandlesLatest200Response)

    #
    # additional query params
    #

    candle_specs: Annotated[
        tuple[CandleSpec, ...],
        query_param(
            ..., alias="candleSpecifications",
            transport_type=TransportCandleSpecSeq,
            description="""Candle specifications for the quotes request

            Syntax:

            value ::= spec[,spec]

            spec ::= instrument:[granularity]:[component]

            instrument: instrument name, e.g GBP_CHF or GBPCHF

            granularity: candlestick granularity, optional. e.g M1,
            H4, M for Monthly granularity, etc. If no granularity is
            specified,  the default granularity  "S5"  will be used

            component: price component string, a concatenation of any of
            A, B, and M, denoting ask, bid, or mid (median) components
            for the  request, e.g A, B, AB, ABM. If no component is
            specified, the default component "mid" will be used
            """
        )
    ]


__all__ = exporting(__name__, ...)
