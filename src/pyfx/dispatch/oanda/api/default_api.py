# DefaultApi definition, based on code generated with OpenAPI Generator

from contextlib import asynccontextmanager
from types import CoroutineType, FunctionType
from typing import Literal
import asyncio as aio
from datetime import datetime
from typing import (
    Any, AsyncIterator, AsyncGenerator, Awaitable,
    Callable, Optional, Union, Mapping, Sequence
)

from typing_extensions import Annotated

from pydantic import Field

from ..util import exporting
from ..exec_controller import ExecController
from ..transport.data import ApiObject
from .. import models
from ..models.response_mixins import ErrorResponse

from ..models import (
    AccountId,
    InstrumentName,
    CancelOrder200Response,
    ClosePosition200Response,
    ClosePositionRequest,
    CloseTrade200Response,
    CloseTradeRequest,
    ConfigureAccount200Response,
    ConfigureAccountRequest,
    CreateOrder201Response,
    CreateOrderRequest,
    GetAccount200Response,
    GetAccountChanges200Response,
    GetAccountInstruments200Response,
    GetAccountSummary200Response,
    GetExternalUserInfo200Response,
    GetInstrumentCandles200Response,
    GetInstrumentPrice200Response,
    GetInstrumentPriceRange200Response,
    GetOrder200Response,
    GetPosition200Response,
    GetPrices200Response,
    GetTrade200Response,
    GetTransaction200Response,
    GetTransactionRange200Response,
    GetUserInfo200Response,
    InstrumentsInstrumentOrderBookGet200Response,
    InstrumentsInstrumentPositionBookGet200Response,
    ListAccounts200Response,
    ListOpenPositions200Response,
    ListOpenTrades200Response,
    ListOrders200Response,
    ListPendingOrders200Response,
    ListPositions200Response,
    ListTrades200Response,
    ListTransactions200Response,
    ReplaceOrder201Response,
    SetOrderClientExtensions200Response,
    SetOrderClientExtensionsRequest,
    SetTradeClientExtensions200Response,
    SetTradeClientExtensionsRequest,
    SetTradeDependentOrders200Response,
    SetTradeDependentOrdersRequest,
    StreamTransactions200Response,
    DayOfWeek
    ) # type: ignore

from ..models.common_types import Time


from ..api_client import ApiClient
from ..request_constants import RequestMethod
from ..response_common import ResponseInfo
from ..parser import ModelBuilder

from .price_component import PriceComponent, ensure_price_component, PriceComponentExpr

def validate_request(func: Callable):
    ## conditional dispatch for enabling validation in
    ## each request method call with pydantic v2
    if __debug__:
        ## pydantic may not be able to parse AsyncGenerator types in args
        # return validate_call(func)
        return func
    else:
        return func


##
## additional base types, constants
##

DT_ORDINAL_ONE: datetime = datetime.fromordinal(1)


class ApiController(ExecController):
    """
    API integration for ExecController

    ## Usage

    As an extension to the abstract ExecController
    class, DispatchController provides additional
    support for initializing an API client to the
    controller.

    Given a subclass implementing `run_async()`,
    the subclass can be used with the ExecController
    `run_context()` context manager. A brief illustration
    is provided in the documentation string for
    `ExecController.run_context()`

    Example are provided in `quotes_app.py` and
    `quotes_async.py` within the `examples`
    source directory
    """

    api_client: ApiClient
    api: "DefaultApi"

    def initialize_defaults(self):
        """
        Initialize all defaults for the base class, then creating
        the ApiClient and DefaultApi for this controller.

        ## Usage

        It's assumed that the `configuration` property will have been
        set, before this method is called.

        The generalized constructor `from_config_ini()` will provide
        a configuration object to the initialized controller.

        This `configuration` object is required for normal API client
        initialization.
        """
        super().initialize_defaults()
        self.api_client = ApiClient(self)
        self.api = DefaultApi(self)

    def close(self):
        """
        Close this controller

        `close()` will close the REST client for this controller,
        then dispatching to `ExecController.close()`
        """
        self.main_loop.run_until_complete(self.api_client.rest_client.aclose())
        super().close()

    @asynccontextmanager
    async def task_context(self):
        async with super().task_context() as tg:
            async with self.api_client.rest_client.client:
                yield tg


##
## Main Code
##

class DefaultApi(object):
    """
    API manager for the fxTrade v20 REST API
    """

    api_client: ApiClient
    """
    API Client for this API manager
    """

    controller: ApiController
    """
    Application dispatch controller for this API manager
    """

    def __init__(self, controller: ApiController):
        """
        Initialize the controller and API Client for this API manager
        """
        self.controller = controller
        self.api_client = controller.api_client

    @classmethod
    def get_streaming_type_callback(self, response_map: Mapping[int, type[ApiObject]],
                                    callback_heartbeat: bool = False
                                    ) -> Callable[[ResponseInfo, bytes], Optional[type[ApiObject]]]:
        heartbeat_cls = response_map[0]
        primary_cls = response_map[200]
        initial_chunk = True
        ## return a callback for ..parser.ModelBuilder.from_receiver_gen()
        ## under the case of a streaming endpoint
        ##
        ## Caveats:
        ## - Under a succesful response, the streaming endpoint will feed
        ##   a series of JSON-encoded objects, terminating once the stream
        ##   is closed. Each object will either have type: "HEARTBEAT"
        ##   or type:<primary> for <primary> denoting the primary class
        ##   of the streaming endpoint
        ##
        ## - The heartbeat class and primary class can be generalized
        ##   across both of the available streaming endpoints. Here,
        ##   index [0] is used for indicating the heartbeat class,
        ##   with index [200] as the primary class in the response
        ##   types map
        ##
        ## - Under an unsuccesful response, the response code will not be 200.
        ##   The status code may or may not match a non-200, non-zero value
        ##   in the response types map. If the response code does not match,
        ##   the callback can return None. The ModelBuilder generator would
        ##   then use a generic JSON decoding to represent the response object
        ##   as an exception under the generator
        ##
        ## - If the request resulted in a non-JSON value in response, e.g
        ##   from an intermediate proxy server, the ModelBuilder generator
        ##   will have handled this internal to the generator routine

        def streaming_type_callback(info: ResponseInfo, chunk: bytes) -> Optional[type[ApiObject]]:
            nonlocal response_map, heartbeat_cls, primary_cls, initial_chunk, callback_heartbeat
            status = info.status
            if initial_chunk:
                initial_chunk = False
                if status is int(200):
                    return primary_cls
                elif status in response_map:
                    return response_map[status]
                else:
                    return None
            elif b'HEARTBEAT' in chunk:
                return heartbeat_cls if callback_heartbeat else None
            else:
                return primary_cls

        return streaming_type_callback

    @classmethod
    def get_rest_type_callback(self, response_map: Mapping[int, type[ApiObject]]
                               ) -> Callable[[ResponseInfo, bytes], Optional[type[ApiObject]]]:


        def rest_type_callback(info: ResponseInfo, chunk: bytes
                               ) -> Optional[type[ApiObject]]:
            nonlocal response_map
            status = info.status
            if status in response_map:
                return response_map[status]

        return rest_type_callback

    @validate_request
    async def cancel_order(self,
                           account_id: AccountId,
                           order_specifier: str,
                           client_request_id: Optional[str] = None,
                           future: Optional[aio.Future[CancelOrder200Response]] = None
                           ) -> Awaitable[CancelOrder200Response]:
        """Cancel Order

        Cancel a pending Order in an Account

        >>> response = api.cancel_order(account_id, order_specifier, client_request_id)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param order_specifier: The Order Specifier (required)
        :type order_specifier: str
        :param client_request_id: Client specified RequestID to be sent with request.
        :type client_request_id: str
        :return: Returns the response object.
        :rtype: tuple(CancelOrder200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id,
                        'orderSpecifier': order_specifier
                        }

        _header_params = {'ClientRequestID': client_request_id} if client_request_id else None
        _response_types_map = {
            200: models.CancelOrder200Response,
            404: models.CancelOrder404Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/orders/{orderSpecifier}/cancel', RequestMethod.PUT,
            path_params=_path_params,
            header_params=_header_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def close_position(self,
                             account_id: AccountId,
                             instrument: InstrumentName,
                             close_position_body: ClosePositionRequest,
                             future: Optional[aio.Future[ClosePosition200Response]] = None
                             ) -> Awaitable[ClosePosition200Response]:
        """Close Position

        Closeout the open Position for a specific instrument in an Account.

        >>> response = api.close_position(account_id, instrument, close_position_body)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param instrument: Name of the Instrument (required)
        :type instrument: InstrumentName
        :param close_position_body: Representation of how to close the position (required)
        :type close_position_body: ClosePositionRequest
        :return: Returns the response object.
        :rtype: tuple(ClosePosition200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id,
                        'instrument': instrument
                        }

        _body_params = close_position_body

        _response_types_map = {
            200: models.ClosePosition200Response,
            400: models.ClosePosition400Response,
            404: models.ClosePosition404Response,
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/positions/{instrument}/close', RequestMethod.PUT,
            path_params=_path_params,
            body=_body_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def close_trade(self,
                          account_id: AccountId,
                          trade_specifier: str,
                          close_trade_body: CloseTradeRequest,
                          future: Optional[aio.Future[CloseTrade200Response]] = None
                          ) -> Awaitable[CloseTrade200Response]:
        """Close Trade

        Close (partially or fully) a specific open Trade in an Account

        >>> response = api.close_trade(account_id, trade_specifier, close_trade_body)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param trade_specifier: Specifier for the Trade (required)
        :type trade_specifier: str
        :param close_trade_body: Details of how much of the open Trade to close. (required)
        :type close_trade_body: CloseTradeRequest
        :return: Returns the response object.
        :rtype: tuple(CloseTrade200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id,
                        'tradeSpecifier': trade_specifier
                        }

        _body_params = close_trade_body

        _response_types_map = {
            200: models.CloseTrade200Response,
            400: models.CloseTrade400Response,
            404: models.CloseTrade404Response,
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/trades/{tradeSpecifier}/close', RequestMethod.PUT,
            path_params=_path_params,
            body=_body_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def configure_account(self,
                                account_id: AccountId,
                                configure_account_body: ConfigureAccountRequest,
                                future: Optional[aio.Future[ConfigureAccount200Response]] = None
                                ) -> Awaitable[ConfigureAccount200Response]:
        """Configure Account

        Set the client-configurable portions of an Account.

        >>> response = api.configure_account(account_id, configure_account_body)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param configure_account_body: Representation of the Account configuration to set
        :type configure_account_body: ConfigureAccountRequest
        :return: Returns the response object.
        :rtype: tuple(ConfigureAccount200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _body_params = configure_account_body

        _response_types_map = {
            200: models.ConfigureAccount200Response,
            400: models.ConfigureAccount400Response,
            403: models.ConfigureAccount400Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/configuration', RequestMethod.PATCH,
            path_params=_path_params,
            body=_body_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def create_order(self,
                           account_id: AccountId,
                           create_order_body: CreateOrderRequest,
                           future: Optional[aio.Future[CreateOrder201Response]] = None
                           ) -> Awaitable[CreateOrder201Response]:
        """Create Order

        Create an Order for an Account

        >>> response = api.create_order(account_id, create_order_body)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param create_order_body: (required)
        :type create_order_body: CreateOrderRequest
        :return: Returns the response object.
        :rtype: tuple(CreateOrder201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _body_params = create_order_body

        _response_types_map = {
            201: models.CreateOrder201Response,
            400: models.CreateOrder400Response,
            404: models.CreateOrder404Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/orders', RequestMethod.POST,
            path_params=_path_params,
            body=_body_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def get_account(self,
                          account_id: AccountId,
                          future: Optional[aio.Future[GetAccount200Response]] = None
                          ) -> Awaitable[GetAccount200Response]:
        """Account Details

        Get the full details for a single Account that a client has access to. Full pending Order, open Trade and open Position representations are provided.

        >>> response = api.get_account(account_id)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :return: Returns the response object.
        :rtype: tuple(GetAccount200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _response_types_map = {
            200: models.GetAccount200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}', RequestMethod.GET,
            path_params=_path_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def get_account_changes(self,
                                  account_id: AccountId,
                                  since_transaction_id: Optional[str] = None,
                                  future: Optional[aio.Future[GetAccountChanges200Response]] = None
                                  ) -> Awaitable[GetAccountChanges200Response]:
        """Poll Account Updates

        Endpoint used to poll an Account for its current state and changes since a specified TransactionID.

        >>> response = api.get_account_changes(account_id, since_transaction_id)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId

        :param since_transaction_id: ID of the Transaction to get Account changes since.
        :type since_transaction_id: str

        :param future
        :type Optional[asyncio.Future[GetAccountChanges200Response]]

        :return: Returns the response object, or None if a future was provided
        :rtype: tuple(GetAccountChanges200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _query_params: Optional[dict[str, Any]] = {'sinceTransactionID': since_transaction_id} if since_transaction_id else None

        _response_types_map = {
            200: models.GetAccountChanges200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/changes', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def get_account_instruments(self,
                                      account_id: AccountId,
                                      instruments: Optional[Sequence[str]] = None,
                                      future: Optional[aio.Future[GetAccountInstruments200Response]] = None
                                      ) -> Awaitable[GetAccountInstruments200Response]:
        """Account Instruments

        Get the list of tradeable instruments for the given Account. The list of tradeable instruments is dependent on the regulatory division that the Account is located in, thus should be the same for all Accounts owned by a single user.

        >>> response = api.get_account_instruments(account_id, instruments)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param instruments: List of instruments to query specifically.
        :type instruments: List[str]
        :return: Returns the response object.
        :rtype: tuple(GetAccountInstruments200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _query_params: Optional[dict[str, Any]] = {'instruments': instruments} if instruments else None
        _collection_formats = {'instruments': 'csv'} if instruments else None

        _response_types_map = {
            200: models.GetAccountInstruments200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/instruments', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map,
            collection_formats=_collection_formats, future=future)

    @validate_request
    async def instruments(self, account_id: AccountId
                          ) -> AsyncIterator[models.Instrument]:
        api_response = await self.get_account_instruments(account_id)
        instruments = api_response.instruments
        if instruments:
            for instrument in instruments:
                yield instrument

    @validate_request
    async def get_account_summary(self,
                                  account_id: AccountId,
                                  future: Optional[aio.Future[GetAccountSummary200Response]] = None
                                  ) -> Awaitable[GetAccountSummary200Response]:
        """Account Summary

        Get a summary for a single Account that a client has access to.

        >>> response = api.get_account_summary(account_id)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :return: Returns the response object.
        :rtype: tuple(GetAccountSummary200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _response_types_map = {
            200: models.GetAccountSummary200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/summary', RequestMethod.GET,
            path_params=_path_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def get_base_prices(self,
                              time: Optional[str] = None,
                              future: Optional[aio.Future[GetInstrumentPriceRange200Response]] = None
                              ) -> Awaitable[GetInstrumentPriceRange200Response]:
        """Get Base Prices

        Get pricing information for a specified instrument. Accounts are not associated in any way with this endpoint.

        >>> response = api.get_base_prices(accept_datetime_format, time)

        :param time: The time at which the desired price for each instrument is in effect. The current price for each instrument is returned if no time is provided.
        :type time: str
        :return: Returns the response object.
        :rtype: tuple(GetInstrumentPriceRange200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _query_params: Optional[dict[str, Any]] = {'time': time} if time else None

        _response_types_map = {
            200: models.GetInstrumentPriceRange200Response
        }

        return await self.api_client.call_api(
            '/pricing', RequestMethod.GET,
            query_params=_query_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def get_external_user_info(self,
                                     user_specifier: str,
                                     future: Optional[aio.Future[GetExternalUserInfo200Response]] = None
                                     ) -> Awaitable[GetExternalUserInfo200Response]:
        """External User Info

        Fetch the externally-available user information for the specified user. This endpoint is intended to be used by 3rd parties that have been authorized by a user to view their personal information.

        >>> response = api.get_external_user_info(user_specifier)

        :param user_specifier: The User Specifier (required)
        :type user_specifier: str
        :return: Returns the response object.
        :rtype: tuple(GetExternalUserInfo200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'userSpecifier': user_specifier}

        _response_types_map = {
            200: models.GetExternalUserInfo200Response
        }

        return await self.api_client.call_api(
            '/users/{userSpecifier}/externalInfo', RequestMethod.GET,
            path_params=_path_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def get_instrument_candles(self,
                                     instrument: InstrumentName,
                                     price: Optional[PriceComponentExpr] = None,
                                     granularity: Optional[models.CandlestickGranularity] = models.CandlestickGranularity.S5,
                                     count: Optional[int] = None,
                                     var_from: Optional[Time] = None,
                                     to: Optional[Time] = None,
                                     smooth: Optional[bool] = None,
                                     include_first: Optional[bool] = None,
                                     daily_alignment: Optional[int] = None,
                                     alignment_timezone: Optional[str] = None,
                                     weekly_alignment: Optional[DayOfWeek] = None,
                                     future: Optional[aio.Future[GetInstrumentCandles200Response]] = None
                                     ) -> Awaitable[GetInstrumentCandles200Response]:
        """Get Candlesticks

        Fetch candlestick data for an instrument.

        >>> response = api.get_instrument_candles(instrument, price, granularity, count, var_from, to, smooth, include_first, daily_alignment, alignment_timezone, weekly_alignment)

        :param instrument: Name of the Instrument (required)
        :type instrument: InstrumentName
        :param price: The Price component(s) for the candlestick data request. May be one of PriceComponent.Median (default), PriceComponent.Ask, PriceComponent.Bid, or a sequence of similar PriceComponent
        :type price: PriceComponent
        :param granularity: The granularity of the candlesticks to fetch
        :type models.CandlestickGranularity: str
        :param count: The number of candlesticks to return in the reponse. Count should not be specified if both the start and end parameters are provided, as the time range combined with the graularity will determine the number of candlesticks to return.
        :type count: int
        :param var_from: The start of the time range to fetch candlesticks for.
        :type var_from: str
        :param to: The end of the time range to fetch candlesticks for.
        :type to: str
        :param smooth: A flag that controls whether the candlestick is \"smoothed\" or not.  A smoothed candlestick uses the previous candle's close price as its open price, while an unsmoothed candlestick uses the first price from its time range as its open price.
        :type smooth: bool
        :param include_first: A flag that controls whether the candlestick that is covered by the from time should be included in the results. This flag enables clients to use the timestamp of the last completed candlestick received to poll for future candlesticks but avoid receiving the previous candlestick repeatedly.
        :type include_first: bool
        :param daily_alignment: The hour of the day (in the specified timezone) to use for granularities that have daily alignments.
        :type daily_alignment: int
        :param alignment_timezone: The timezone to use for the dailyAlignment parameter. Candlesticks with daily alignment will be aligned to the dailyAlignment hour within the alignmentTimezone.  Note that the returned times will still be represented in UTC.
        :type alignment_timezone: str
        :param weekly_alignment: The day of the week used for granularities that have weekly alignment.
        :type weekly_alignment: str
        :return: Returns the response object.
        :rtype: tuple(GetInstrumentCandles200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'instrument': instrument}

        _query_params: dict[str, Any] = dict()
        if price:
            _query_params['price'] = ensure_price_component(price)

        if granularity:
            _query_params['granularity'] = granularity

        if count:
            _query_params['count'] = count

        if var_from:
            _query_params['from'] = var_from

        if to:
            _query_params['to'] = to

        if smooth:
            _query_params['smooth'] = smooth

        if include_first:
            _query_params['includeFirst'] = include_first

        if daily_alignment:
            _query_params['dailyAlignment'] = daily_alignment

        if alignment_timezone:
            _query_params['alignmentTimezone'] = alignment_timezone

        if weekly_alignment:
            _query_params['weeklyAlignment'] = weekly_alignment

        _response_types_map = {
            200: models.GetInstrumentCandles200Response
        }

        return await self.api_client.call_api(
            '/instruments/{instrument}/candles', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def candles(self,
                      instrument: InstrumentName,
                      price: Optional[Union[PriceComponent, str]] = None,
                      granularity: Optional[models.CandlestickGranularity] = None,
                      count: Optional[int] = None,
                      var_from: Optional[str] = None,
                      to: Optional[str] = None,
                      smooth: Optional[bool] = None,
                      include_first: Optional[bool] = None,
                      daily_alignment: Optional[int] = None,
                      alignment_timezone: Optional[str] = None,
                      weekly_alignment: Optional[str] = None
                      ) -> AsyncIterator[models.Candlestick]:
        api_response = await self.get_instrument_candles(instrument, price, granularity, count, var_from, to, smooth, include_first, daily_alignment, alignment_timezone, weekly_alignment)
        candles = api_response.candles
        if candles:
            async for candle in candles:
                yield candle

    @validate_request
    async def get_instrument_candles_by_account(self,
                                                account_id: AccountId,
                                                instrument: InstrumentName,
                                                price: Optional[PriceComponentExpr] = None,
                                                granularity: Optional[models.CandlestickGranularity] = None,
                                                count: Optional[int] = None,
                                                var_from: Optional[str] = None,
                                                to: Optional[str] = None,
                                                smooth: Optional[bool] = None,
                                                include_first: Optional[bool] = None,
                                                daily_alignment: Optional[int] = None,
                                                alignment_timezone: Optional[str] = None,
                                                weekly_alignment: Optional[str] = None,
                                                units: Optional[str] = None,
                                                future: Optional[aio.Future[GetInstrumentCandles200Response]] = None
                                                ) -> Awaitable[GetInstrumentCandles200Response]:
        """Get Candlesticks using account ID

        Retrieve candlestick data for an instrument, using a provided account identifier. The instrument
        request parameters are the same as with get_instrument_candles()

        >>> response = api.get_instrument_candles_0(instrument, price, granularity, count, var_from, to, smooth, include_first, daily_alignment, alignment_timezone, weekly_alignment, units)

        :param instrument: Name of the Instrument (required)
        :type instrument: InstrumentName
        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param price: The Price component(s) for the candlestick data request. May be one of PriceComponent.Median (default), PriceComponent.Ask, PriceComponent.Bid, or a sequence of similar PriceComponent
        :type price: PriceComopnent
        :param granularity: The granularity of the candlesticks to fetch
        :type granularity: str
        :param count: The number of candlesticks to return in the response. Count should not be specified if both the start and end parameters are provided, as the time range combined with the granularity will determine the number of candlesticks to return.
        :type count: int
        :param var_from: The start of the time range to fetch candlesticks for.
        :type var_from: str
        :param to: The end of the time range to fetch candlesticks for.
        :type to: str
        :param smooth: A flag that controls whether the candlestick is \"smoothed\" or not.  A smoothed candlestick uses the previous candle's close price as its open price, while an unsmoothed candlestick uses the first price from its time range as its open price.
        :type smooth: bool
        :param include_first: A flag that controls whether the candlestick that is covered by the from time should be included in the results. This flag enables clients to use the timestamp of the last completed candlestick received to poll for future candlesticks but avoid receiving the previous candlestick repeatedly.
        :type include_first: bool
        :param daily_alignment: The hour of the day (in the specified timezone) to use for granularities that have daily alignments.
        :type daily_alignment: int
        :param alignment_timezone: The timezone to use for the dailyAlignment parameter. Candlesticks with daily alignment will be aligned to the dailyAlignment hour within the alignmentTimezone.  Note that the returned times will still be represented in UTC.
        :type alignment_timezone: str
        :param weekly_alignment: The day of the week used for granularities that have weekly alignment.
        :type weekly_alignment: str
        :param units: The number of units used to calculate the volume-weighted average bid and ask prices in the returned candles.
        :type units: str
        :return: Returns the response object.
        :rtype: tuple(GetInstrumentCandles200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {
            'instrument': instrument,
            "accountID": account_id
        }

        _query_params: dict[str, Any] = dict()
        if price:
            _query_params['price'] = ensure_price_component(price)

        if granularity:
            _query_params['granularity'] = granularity

        if count:
            _query_params['count'] = count

        if var_from:
            _query_params['from'] = var_from

        if to:
            _query_params['to'] = to

        if smooth:
            _query_params['smooth'] = smooth

        if include_first:
            _query_params['includeFirst'] = include_first

        if daily_alignment:
            _query_params['dailyAlignment'] = daily_alignment

        if alignment_timezone:
            _query_params['alignmentTimezone'] = alignment_timezone

        if weekly_alignment:
            _query_params['weeklyAlignment'] = weekly_alignment

        if units:
            _query_params['units'] = units

        _response_types_map = {
            200: models.GetInstrumentCandles200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/instruments/{instrument}/candles', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def candles_by_account(self,
                                 account_id: AccountId,
                                 instrument: InstrumentName,
                                 price: Optional[Union[PriceComponent, str]] = None,
                                 granularity: Optional[models.CandlestickGranularity] = None,
                                 count: Optional[int] = None,
                                 var_from: Optional[str] = None,
                                 to: Optional[str] = None,
                                 smooth: Optional[bool] = None,
                                 include_first: Optional[bool] = None,
                                 daily_alignment: Optional[int] = None,
                                 alignment_timezone: Optional[str] = None,
                                 weekly_alignment: Optional[str] = None
                      ) -> AsyncIterator[models.Candlestick]:
        api_response = await self.get_instrument_candles_by_account(account_id, instrument, price, granularity, count, var_from, to, smooth, include_first, daily_alignment, alignment_timezone, weekly_alignment)
        candles = api_response.candles
        if candles:
            async for candle in candles:
                yield candle

    @validate_request
    async def get_instrument_price(self,
                                   instrument: InstrumentName,
                                   time: Optional[datetime] = None,
                                   future: Optional[aio.Future[GetInstrumentPrice200Response]] = None
                                   ) -> Awaitable[GetInstrumentPrice200Response]:
        """Price

        [**Deprecated**]

        This endpoint was defined in the fxTrade v20 API release 3.0.25, and may not be supported at this time.

        See alternately: DefaultApi.get_prices(), DefaultApi.stream_pricing()


        Fetch a price for an instrument. Accounts are not associated in any way with this endpoint.

        >>> response = api.get_instrument_price(instrument, time)

        :param instrument: Name of the Instrument (required)
        :type instrument: InstrumentName
        :param time: The time at which the desired price is in effect. The current price is returned if no time is provided.
        :type time: str
        :return: Returns the response object.
        :rtype: tuple(GetInstrumentPrice200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'instrument': instrument}

        _query_params: Optional[dict[str, Any]] = {'time': time} if time else None

        _response_types_map = {
            200: models.GetInstrumentPrice200Response
        }

        return await self.api_client.call_api(
            '/instruments/{instrument}/price', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def get_instrument_price_range(self,
                                         instrument: InstrumentName,
                                         var_from: str,
                                         to: Optional[str] = None,
                                         future: Optional[aio.Future[GetInstrumentPriceRange200Response]] = None
                                         ) -> Awaitable[GetInstrumentPriceRange200Response]:
        """Get Prices

        [**Deprecated**]

        This endpoint was defined in the fxTrade v20 API release 3.0.25, and may not be supported at this time.

        See alternately: DefaultApi.get_prices(), DefaultApi.stream_pricing()


        Fetch a range of prices for an instrument. Accounts are not associated in any way with this endpoint.

        >>> response = api.get_instrument_price_range(instrument, var_from, to)

        :param instrument: Name of the Instrument (required)
        :type instrument: InstrumentName
        :param var_from: The start of the time range to fetch prices for. (required)
        :type var_from: str
        :param to: The end of the time range to fetch prices for. The current time is used if this parameter is not provided.
        :type to: str
        :return: Returns the response object.
        :rtype: tuple(GetInstrumentPriceRange200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'instrument': instrument}

        _query_params: dict[str, Any] = {'from': var_from}

        if to:
            _query_params['to'] = to

        _response_types_map = {
            200: models.GetInstrumentPriceRange200Response
        }

        return await self.api_client.call_api(
            '/instruments/{instrument}/price/range', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def get_order(self,
                        account_id: AccountId,
                        order_specifier: str,
                        future: Optional[aio.Future[GetOrder200Response]] = None
                        ) -> Awaitable[GetOrder200Response]:
        """Get Order

        Get details for a single Order in an Account

        >>> response = api.get_order(account_id, order_specifier)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param order_specifier: The Order Specifier (required)
        :type order_specifier: str
        :return: Returns the response object.
        :rtype: tuple(GetOrder200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id,
                        'orderSpecifier': order_specifier
                        }

        _response_types_map = {
            200: models.GetOrder200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/orders/{orderSpecifier}', RequestMethod.GET,
            path_params=_path_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def get_position(self,
                           account_id: AccountId,
                           instrument: InstrumentName,
                           future: Optional[aio.Future[GetPosition200Response]] = None
                           ) -> Awaitable[GetPosition200Response]:
        """Instrument Position

        Get the details of a single Instrument's Position in an Account. The Position may by open or not.

        >>> response = api.get_position(account_id, instrument)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param instrument: Name of the Instrument (required)
        :type instrument: InstrumentName
        :return: Returns the response object.
        :rtype: tuple(GetPosition200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        if instrument:
            _path_params['instrument'] = instrument

        _response_types_map = {
            200: models.GetPosition200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/positions/{instrument}', RequestMethod.GET,
            path_params=_path_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def get_price_range(self,
                              instrument: InstrumentName,
                              var_from: str,
                              to: Optional[str] = None,
                              future: Optional[aio.Future[GetInstrumentPriceRange200Response]] = None
                              ) -> Awaitable[GetInstrumentPriceRange200Response]:
        """Get Price Range


        Get pricing information for a specified range of prices. Accounts are not associated in any way with this endpoint.

        >>> response = api.get_price_range(instrument, var_from, to)

        :param instrument: Name of the Instrument (required)
        :type instrument: InstrumentName
        :param var_from: The start of the time range to fetch prices for. (required)
        :type var_from: str
        :param to: The end of the time range to fetch prices for. The current time is used if this parameter is not provided.
        :type to: str
        :return: Returns the response object.
        :rtype: tuple(GetInstrumentPriceRange200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'instrument': instrument}

        _query_params: dict[str, Any] = dict()
        if var_from:
            _query_params['from'] = var_from

        if to:
            _query_params['to'] = to

        _response_types_map = {
            200: models.GetInstrumentPriceRange200Response
        }

        return await self.api_client.call_api(
            '/pricing/range', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def get_prices(self,
                         account_id: AccountId,
                         instruments: Sequence[str],
                         since: Optional[str] = None,
                         include_units_available: Optional[bool] = None,
                         include_home_conversions: Optional[bool] = None,
                         future: Optional[aio.Future[GetPrices200Response]] = None
                         ) -> Awaitable[GetPrices200Response]:
        """Current Account Prices


        Get pricing information for a specified list of Instruments within an Account.

        >>> response = api.get_prices(account_id, instruments, since, include_units_available, include_home_conversions)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param instruments: List of Instruments to get pricing for. (required)
        :type instruments: List[str]
        :param since: Date/Time filter to apply to the response. Only prices and home conversions (if requested) with a time later than this filter (i.e. the price has changed after the since time) will be provided, and are filtered independently.
        :type since: str
        :param include_units_available: Flag that enables the inclusion of the unitsAvailable field in the returned Price objects.
        :type include_units_available: bool
        :param include_home_conversions: Flag that enables the inclusion of the homeConversions field in the returned response. An entry will be returned for each currency in the set of all base and quote currencies present in the requested instruments list.
        :type include_home_conversions: bool
        :return: Returns the response object.
        :rtype: tuple(GetPrices200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _query_params: dict[str, Any] = {'instruments': instruments}
        _collection_formats = {'instruments': 'csv'}

        if since:
            _query_params['since'] = since

        if include_units_available:
            _query_params['includeUnitsAvailable'] = include_units_available

        if include_home_conversions:
            _query_params['includeHomeConversions'] = include_home_conversions

        _response_types_map = {
            200: models.GetPrices200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/pricing', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map,
            collection_formats=_collection_formats, future=future)

    @validate_request
    async def get_trade(self,
                        account_id: AccountId,
                        trade_specifier: str,
                        future: Optional[aio.Future[GetTrade200Response]] = None
                        ) -> Awaitable[GetTrade200Response]:
        """Trade Details

        Get the details of a specific Trade in an Account

        >>> response = api.get_trade(account_id, trade_specifier)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param trade_specifier: Specifier for the Trade (required)
        :type trade_specifier: str
        :return: Returns the response object.
        :rtype: tuple(GetTrade200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        if trade_specifier:
            _path_params['tradeSpecifier'] = trade_specifier

        _response_types_map = {
            200: models.GetTrade200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/trades/{tradeSpecifier}', RequestMethod.GET,
            path_params=_path_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def get_transaction(self,
                              account_id: AccountId,
                              transaction_id: str,
                              future: Optional[aio.Future[GetTransaction200Response]] = None
                              ) -> Awaitable[GetTransaction200Response]:
        """Transaction Details

        Get the details of a single Account Transaction.

        >>> response = api.get_transaction(account_id, transaction_id)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param transaction_id: A Transaction ID (required)
        :type transaction_id: str
        :return: Returns the response object.
        :rtype: tuple(GetTransaction200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        if transaction_id:
            _path_params['transactionID'] = transaction_id

        _response_types_map = {
            200: models.GetTransaction200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/transactions/{transactionID}', RequestMethod.GET,
            path_params=_path_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def get_transaction_range(self,
                                    account_id: AccountId,
                                    var_from: str,
                                    to: str,
                                    type_filter: Optional[Sequence[str]] = None,
                                    future: Optional[aio.Future[GetTransactionRange200Response]] = None
                                    ) -> Awaitable[GetTransactionRange200Response]:
        """Transaction ID Range

        Get a range of Transactions for an Account based on the Transaction IDs.

        >>> response = api.get_transaction_range(account_id, var_from, to, type)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param var_from: The starting Transacion ID (inclusive) to fetch. (required)
        :type var_from: str
        :param to: The ending Transaction ID (inclusive) to fetch. (required)
        :type to: str
        :param type_filter: The filter that restricts the types of Transactions to retreive.
        :type type: List[str]
        :return: Returns the response object.
        :rtype: tuple(GetTransactionRange200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _query_params: dict[str, Any] = dict()
        if var_from:
            _query_params['from'] = var_from

        if to:
            _query_params['to'] = to

        if type_filter:
            _query_params['type'] = type_filter

        _collection_formats = {'type': 'csv'} if type_filter else None

        _response_types_map = {
            200: models.GetTransactionRange200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/transactions/idrange', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map,
            collection_formats=_collection_formats, future=future)

    @validate_request
    async def get_transactions_since_id(self,
                                        account_id: AccountId,
                                        txn_id: str,
                                        future: Optional[aio.Future[GetTransactionRange200Response]] = None
                                        ) -> Awaitable[GetTransactionRange200Response]:
        """Transactions Since ID

        Get a range of Transactions for an Account starting at (but not including) a provided Transaction ID.

        >>> response = api.get_transactions_since_id(account_id, id)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param txn_id: The ID of the last Transacion fetched. This query will return all Transactions newer than the TransactionID. (required)
        :type id: str
        :return: Returns the response object.
        :rtype: tuple(GetTransactionRange200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _query_params: dict[str, Any] = (('id', txn_id),)

        _response_types_map = {
            200: models.GetTransactionRange200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/transactions/sinceid', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def get_user_info(self,
                            user_specifier: str,
                            future: Optional[aio.Future[GetUserInfo200Response]] = None
                            ) -> Awaitable[GetUserInfo200Response]:
        """User Info

        [**Deprecated**]

        This endpoint was defined in the fxTrade v20 API release 3.0.25, and may not be supported at this time.

        Fetch the user information for the specified user. This endpoint is intended to be used by the user themself to obtain their own information.

        >>> response = api.get_user_info(user_specifier)

        :param user_specifier: The User Specifier (required)
        :type user_specifier: str
        :return: Returns the response object.
        :rtype: tuple(GetUserInfo200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'userSpecifier': user_specifier}

        _response_types_map = {
            200: models.GetUserInfo200Response
        }

        return await self.api_client.call_api(
            '/users/{userSpecifier}', RequestMethod.GET,
            path_params=_path_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def instruments_instrument_order_book_get(self,
                                                    instrument: InstrumentName,
                                                    time: Optional[str] = None,
                                                    future: Optional[aio.Future[InstrumentsInstrumentOrderBookGet200Response]] = None
                                                    ) -> Awaitable[InstrumentsInstrumentOrderBookGet200Response]:
        """Get Order Book

        [**Limited Availability**]

        This endploint may not be available in fxPractice profiles.

        Fetch an order book for an instrument.

        >>> response = api.instruments_instrument_order_book_get(instrument, time)

        :param instrument: Name of the Instrument (required)
        :type instrument: InstrumentName
        :param time: The time of the snapshot to fetch. If not specified, then the most recent snapshot is fetched.
        :type time: str
        :return: Returns the response object.
        :rtype: tuple(InstrumentsInstrumentOrderBookGet200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'instrument': instrument}

        _query_params: Optional[dict[str, Any]] = {'time': time} if time else None

        _response_types_map = {
            200: models.InstrumentsInstrumentOrderBookGet200Response
        }

        return await self.api_client.call_api(
            '/instruments/{instrument}/orderBook', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def list_accounts(self, future: Optional[aio.Future[ListAccounts200Response]] = None
                            ) -> Awaitable[Optional[ListAccounts200Response]]:
        """List Accounts

        Get a list of all Accounts authorized for the provided token.

        >>> response = api.list_accounts()

        :return: Returns the response object, or None if a generator receiver was provided
        :rtype: tuple(ListAccounts200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _response_types_map = {
            200: models.ListAccounts200Response
        }

        return await self.api_client.call_api(
            '/accounts', RequestMethod.GET,
            response_types_map=_response_types_map,
            future=future)

    @validate_request
    async def accounts(self,
                       ## pydantic entirely fails to parse the AsyncGenerator arg
                       # controller: ApiController, ## for prototyping only @ the arg's presence here ...
                       receiver: Optional[AsyncGenerator[Any, models.AccountProperties]] = None
                       ) -> AsyncIterator[models.AccountProperties]:
        response = await self.list_accounts()
        accounts = response.accounts
        if accounts:
            for ac in accounts:
                yield ac
        else:
            return

    @validate_request
    async def instruments_instrument_position_book_get(self,
                                                       instrument: InstrumentName,
                                                       time: Optional[str] = None,
                                                       future: Optional[aio.Future[InstrumentsInstrumentPositionBookGet200Response]] = None
                                                       ) -> Awaitable[InstrumentsInstrumentPositionBookGet200Response]:
        """Get Position Book

        [**Limited Availability**]

        This endploint may not be available in fxPractice profiles.

        Fetch a position book for an instrument.

        >>> response = api.instruments_instrument_position_book_get(instrument, time)

        :param instrument: Name of the Instrument (required)
        :type instrument: InstrumentName
        :param time: The time of the snapshot to fetch. If not specified, then the most recent snapshot is fetched.
        :type time: str
        :return: Returns the response object.
        :rtype: tuple(InstrumentsInstrumentPositionBookGet200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'instrument': instrument}

        _query_params: Optional[dict[str, Any]] = {'time': time} if time else None

        _response_types_map = {
            200: models.InstrumentsInstrumentPositionBookGet200Response
        }

        return await self.api_client.call_api(
            '/instruments/{instrument}/positionBook', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def list_open_positions(self,
                                  account_id: AccountId,
                                  future: Optional[aio.Future[ListOpenPositions200Response]] = None
                                  ) -> Awaitable[ListOpenPositions200Response]:
        """Open Positions

        List all open Positions for an Account. An open Position is a Position in an Account that currently has a Trade opened for it.

        >>> response = api.list_open_positions(account_id)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :return: Returns the response object.
        :rtype: tuple(ListOpenPositions200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _response_types_map = {
            200: models.ListOpenPositions200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/openPositions', RequestMethod.GET,
            path_params=_path_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def open_positions(self, account_id: AccountId
                             ) -> AsyncIterator[models.Position]:
        response = await self.list_open_positions(account_id)
        positions = response.positions
        if positions:
            for p in positions:
                yield p

    @validate_request
    async def list_open_trades(self, account_id: AccountId,
                               future: Optional[aio.Future[ListOpenTrades200Response]] = None
                               ) -> Awaitable[ListOpenTrades200Response]:
        """List Open Trades

        Get the list of open Trades for an Account

        >>> response = api.list_open_trades(account_id)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :return: Returns the response object.
        :rtype: tuple(ListOpenTrades200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _response_types_map = {
            200: models.ListOpenTrades200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/openTrades', RequestMethod.GET,
            path_params=_path_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def open_trades(self, account_id: AccountId
                          ) -> AsyncIterator[models.Trade]:
        response = await self.list_open_trades(account_id)

    @validate_request
    async def list_orders(self, account_id: AccountId,
                          ids: Optional[Sequence[str]] = None,
                          state: Optional[str] = None,
                          instrument: Optional[str] = None,
                          count: Annotated[Optional[int], Field(json_schema_extra=dict(max=500))] = 50,
                          before_id: Optional[str] = None,
                          future: Optional[aio.Future[ListOrders200Response]] = None
                          ) -> Awaitable[ListOrders200Response]:
        """List Orders

        Get a list of Orders for an Account

        >>> response = api.list_orders(account_id, ids, state, instrument, count, before_id)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId

        :param ids: List of Order IDs to retrieve
        :type ids: List[str]

        :param state: The state to filter the requested Orders by
        :type state: str

        :param instrument: The instrument to filter the requested orders by
        :type instrument: InstrumentName

        :param count: The maximum number of Orders to return (default: 50, maximum: 500)
        :type count: int

        :param before_id: The maximum Order ID to return. If not provided the most recent Orders in the Account are returned
        :type before_id: str

        :return: Returns the response object.
        :rtype: tuple(ListOrders200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _query_params: dict[str, Any] = {'ids': ids} if ids else {}
        _collection_formats = {'ids': 'csv'} if ids else None

        if state:
            _query_params['state'] = state

        if instrument:
            _query_params['instrument'] = instrument

        if count:
            _query_params['count'] = count

        if before_id:
            _query_params['beforeID'] = before_id

        _response_types_map = {
            200: models.ListOrders200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/orders', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map,
            collection_formats=_collection_formats, future=future)

    @validate_request
    async def orders(self,
                     account_id: AccountId,
                     ids: Optional[Sequence[str]] = None,
                     state: Optional[str] = None,
                     instrument: Optional[str] = None,
                     count: Optional[int] = None,
                     before_id: Optional[str] = None) -> AsyncIterator[models.Order]:
        response = await self.list_orders(account_id, ids, state, instrument, count, before_id)
        orders = response.orders
        if orders:
            for o in orders:
                yield o

    @validate_request
    async def list_pending_orders(self, account_id: AccountId,
                                  future: Optional[aio.Future[ListPendingOrders200Response]] = None
                                  ) -> Awaitable[ListPendingOrders200Response]:
        """Pending Orders

        List all pending Orders in an Account

        >>> response = api.list_pending_orders(account_id)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :return: Returns the response object.
        :rtype: tuple(ListPendingOrders200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _response_types_map = {
            200: models.ListPendingOrders200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/pendingOrders', RequestMethod.GET,
            path_params=_path_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def pending_orders(self, account_id: AccountId
                             ) -> AsyncIterator[models.Order]:
        response = await self.pending_orders(account_id)
        orders = response.orders
        if orders:
            for o in orders:
                yield o

    @validate_request
    async def list_positions(self, account_id: AccountId,
                             future: Optional[aio.Future[ListPositions200Response]] = None
                             ) -> Awaitable[ListPositions200Response]:
        """List Positions

        List all Positions for an Account. The Positions returned are for every instrument that has had a position during the lifetime of an the Account.

        >>> response = api.list_positions(account_id)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :return: Returns the response object.
        :rtype: tuple(ListPositions200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _response_types_map = {
            200: models.ListPositions200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/positions', RequestMethod.GET,
            path_params=_path_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def positions(self, account_id: AccountId
                        ) -> AsyncIterator[models.Position]:
        response = await self.list_positions(account_id)
        positions = response.positions
        if positions:
            for p in positions:
                yield p

    @validate_request
    async def list_trades(self,
                          account_id: AccountId,
                          ids: Optional[Sequence[str]] = None,
                          state: Optional[str] = None,
                          instrument: Optional[str] = None,
                          count: Optional[int] = None,
                          before_id: Optional[str] = None,
                          future: Optional[aio.Future[ListTrades200Response]] = None
                          ) -> Awaitable[ListTrades200Response]:
        """List Trades

        Get a list of Trades for an Account

        >>> response = api.list_trades(account_id, ids, state, instrument, count, before_id)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param ids: List of Trade IDs to retrieve.
        :type ids: List[str]
        :param state: The state to filter the requested Trades by.
        :type state: str
        :param instrument: The instrument to filter the requested Trades by.
        :type instrument: InstrumentName
        :param count: The maximum number of Trades to return.
        :type count: int
        :param before_id: The maximum Trade ID to return. If not provided the most recent Trades in the Account are returned.
        :type before_id: str
        :return: Returns the response object.
        :rtype: tuple(ListTrades200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _query_params: dict[str, Any] = {'ids': ids} if ids else {}
        _collection_formats = {'ids': 'csv'} if ids else None

        if state:
            _query_params['state'] = state

        if instrument:
            _query_params['instrument'] = instrument

        if count:
            _query_params['count'] = count

        if before_id:
            _query_params['beforeID'] = before_id

        _response_types_map = {
            200: models.ListTrades200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/trades', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map,
            collection_formats=_collection_formats, future=future)

    @validate_request
    async def trades(self,
                     account_id: AccountId,
                     ids: Optional[Sequence[str]] = None,
                     state: Optional[str] = None,
                     instrument: Optional[str] = None,
                     count: Optional[int] = None,
                     before_id: Optional[str] = None) -> AsyncIterator[models.Trade]:
        response = await self.list_trades(account_id, ids, state, instrument, count, before_id)
        trades = response.trades
        if trades:
            for t in trades:
                yield t

    @validate_request
    async def list_transactions(self,
                                account_id: AccountId,
                                var_from: Optional[str] = None,
                                to: Optional[str] = None,
                                page_size: Annotated[Optional[int], Field(json_schema_extra=dict(max=1000))] = 100,
                                type_filter: Optional[Sequence[str]] = None,
                                future: Optional[aio.Future[ListTransactions200Response]] = None
                                ) -> Awaitable[ListTransactions200Response]:
        """List Transactions

        Get a list of Transactions pages that satisfy a time-based Transaction query.

        >>> response = api.list_transactions(account_id, var_from, to, page_size, type)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param var_from: The starting time (inclusive) of the time range for the Transactions being queried.
        :type var_from: str
        :param to: The ending time (inclusive) of the time range for the Transactions being queried.
        :type to: str
        :param page_size: The number of Transactions to include in each page of the results.
        :type page_size: int
        :param type_filter: A filter for restricting the types of Transactions to retreive.
        :type type: List[str]
        :return: Returns the response object.
        :rtype: tuple(ListTransactions200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _query_params: dict[str, Any] = dict()
        if var_from:
            _query_params['from'] = var_from

        if to:
            _query_params['to'] = to

        if page_size:
            _query_params['pageSize'] = page_size

        if type_filter:
            _query_params['type'] = type_filter

        _collection_formats = {'type': 'csv'} if type_filter else None

        _response_types_map = {
            200: models.ListTransactions200Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/transactions', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            response_types_map=_response_types_map,
            collection_formats=_collection_formats, future=future)

    @validate_request
    async def transactions(self,
                           account_id: AccountId,
                           var_from: datetime = DT_ORDINAL_ONE,
                           to: Optional[datetime] = None,
                           page_size: Annotated[Optional[int], Field(json_schema_extra=dict(max=1000))] = 100,
                           type: Optional[Sequence[models.TransactionFilter]] = None
                           ) -> AsyncIterator[models.Transaction]:
        # Implementation Notes
        #
        # Each item in 'pages' of the response will have to be accessed and deserialized separately.
        #
        # Each page will generally provide a JSON mapping object, with keys 'transactions', 'lastTransactionID"
        #
        # The 'transactions' field will be provided as a JSON sequence of Transaction values
        #
        # API info: https://developer.oanda.com/rest-live-v20/transaction-ep/
        response = await self.list_transactions(account_id, var_from, to, page_size, type)
        pages = response.pages
        if pages:
            for url in pages:
                async with self.api_client.rest_client.client.stream(RequestMethod.GET.value, url) as response:
                    text = ''
                    async for chunk in response.aiter_bytes():
                        text += chunk.decode()
                    # mapping = thunk.load_the_json(text)

    @validate_request
    async def replace_order(self,
                            account_id: AccountId,
                            order_specifier: str,
                            replace_order_body: CreateOrderRequest,
                            client_request_id: Optional[str] = None,
                            future: Optional[aio.Future[ReplaceOrder201Response]] = None
                            ) -> Awaitable[ReplaceOrder201Response]:
        """Replace Order

        Replace an Order in an Account by simultaneously cancelling it and creating a replacement Order

        >>> response = api.replace_order(account_id, order_specifier, replace_order_body, client_request_id)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param order_specifier: The Order Specifier (required)
        :type order_specifier: str
        :param replace_order_body: Specification of the replacing Order. The replacing order must have the same type as the replaced Order. (required)
        :type replace_order_body: CreateOrderRequest
        :param client_request_id: Client specified RequestID to be sent with request.
        :type client_request_id: str
        :return: Returns the response object.
        :rtype: tuple(ReplaceOrder201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        if order_specifier:
            _path_params['orderSpecifier'] = order_specifier

        _header_params = {'ClientRequestID': client_request_id} if client_request_id else None

        _body_params = replace_order_body

        _response_types_map = {
            201: models.ReplaceOrder201Response,
            400: models.ReplaceOrder400Response,
            404: models.ReplaceOrder404Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/orders/{orderSpecifier}', RequestMethod.PUT,
            path_params=_path_params,
            header_params=_header_params,
            body=_body_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def set_order_client_extensions(self,
                                          account_id: AccountId,
                                          order_specifier: str,
                                          set_order_client_extensions_body: SetOrderClientExtensionsRequest,
                                          future: Optional[aio.Future[SetOrderClientExtensions200Response]] = None
                                          ) -> Awaitable[SetOrderClientExtensions200Response]:
        """Set Order Extensions

        Update the Client Extensions for an Order in an Account.

        Do not set, modify, or delete clientExtensions if your account is associated with MT4.

        >>> response = api.set_order_client_extensions(account_id, order_specifier, set_order_client_extensions_body)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param order_specifier: The Order Specifier (required)
        :type order_specifier: str
        :param set_order_client_extensions_body: Representation of the replacing Order (required)
        :type set_order_client_extensions_body: SetOrderClientExtensionsRequest
        :return: Returns the response object.
        :rtype: tuple(SetOrderClientExtensions200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        if order_specifier:
            _path_params['orderSpecifier'] = order_specifier

        _body_params = set_order_client_extensions_body

        _response_types_map = {
            200: models.SetOrderClientExtensions200Response,
            400: models.SetOrderClientExtensions400Response,
            404: models.SetOrderClientExtensions404Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/orders/{orderSpecifier}/clientExtensions', RequestMethod.PUT,
            path_params=_path_params,
            body=_body_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def set_trade_client_extensions(self,
                                          account_id: AccountId,
                                          trade_specifier: str,
                                          set_trade_client_extensions_body: SetTradeClientExtensionsRequest,
                                          future: Optional[aio.Future[SetTradeClientExtensions200Response]] = None
                                          ) -> Awaitable[SetTradeClientExtensions200Response]:
        """Set Trade Client Extensions

        Update the Client Extensions for a Trade. Do not add, update, or delete the Client Extensions if your account is associated with MT4.

        >>> response = api.set_trade_client_extensions(account_id, trade_specifier, set_trade_client_extensions_body)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param trade_specifier: Specifier for the Trade (required)
        :type trade_specifier: str
        :param set_trade_client_extensions_body: Details of how to modify the Trade's Client Extensions. (required)
        :type set_trade_client_extensions_body: SetTradeClientExtensionsRequest
        :return: Returns the response object.
        :rtype: tuple(SetTradeClientExtensions200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        if trade_specifier:
            _path_params['tradeSpecifier'] = trade_specifier

        _body_params = set_trade_client_extensions_body

        _response_types_map = {
            200: models.SetTradeClientExtensions200Response,
            400: models.SetTradeClientExtensions400Response,
            404: models.SetTradeClientExtensions404Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/trades/{tradeSpecifier}/clientExtensions', RequestMethod.PUT,
            path_params=_path_params,
            body=_body_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def set_trade_dependent_orders(self,
                                         account_id: AccountId,
                                         trade_specifier: str,
                                         set_trade_dependent_orders_body: SetTradeDependentOrdersRequest,
                                         future: Optional[aio.Future[SetTradeDependentOrders200Response]] = None
                                         ) -> Awaitable[SetTradeDependentOrders200Response]:
        """Set Dependent Orders

        Create, replace and cancel a Trade's dependent Orders (Take Profit, Stop Loss and Trailing Stop Loss) through the Trade itself

        >>> response = api.set_trade_dependent_orders(account_id, trade_specifier, set_trade_dependent_orders_body)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param trade_specifier: Specifier for the Trade (required)
        :type trade_specifier: str
        :param set_trade_dependent_orders_body: Details of how to modify the Trade's dependent Orders. (required)
        :type set_trade_dependent_orders_body: SetTradeDependentOrdersRequest
        :return: Returns the response object.
        :rtype: tuple(SetTradeDependentOrders200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        if trade_specifier:
            _path_params['tradeSpecifier'] = trade_specifier

        _body_params = set_trade_dependent_orders_body

        _response_types_map = {
            200: models.SetTradeDependentOrders200Response,
            400: models.SetTradeDependentOrders400Response
        }

        return await self.api_client.call_api(
            '/accounts/{accountID}/trades/{tradeSpecifier}/orders', RequestMethod.PUT,
            path_params=_path_params,
            body=_body_params,
            response_types_map=_response_types_map, future=future)

    @validate_request
    async def stream_pricing(self,
                             model_callback: Callable[[ApiObject], Any],
                             account_id: AccountId, instruments: Sequence[str],
                             snapshot: Optional[bool] = None,
                             callback_heartbeat: bool = False,
                             future: Optional[aio.Future[Literal[True]]] = None
                             ):  # -> Awaitable[StreamPricing200Response]:
        """Price Stream

        Get a stream of Account Prices starting from when the request is made. This pricing stream does not include every single price created for the Account, but instead will provide at most 4 prices per second (every 250 milliseconds) for each instrument being requested. If more than one price is created for an instrument during the 250 millisecond window, only the price in effect at the end of the window is sent. This means that during periods of rapid price movement, subscribers to this stream will not be sent every price. Pricing windows for different connections to the price stream are not all aligned in the same way (i.e. they are not all aligned to the top of the second). This means that during periods of rapid price movement, different subscribers may observe different prices depending on their alignment.

        >>> response = api.stream_pricing(account_id, instruments, snapshot)


        :param model_callback: Callback for model objects. This callback will called for each
               normal response object decoded from the streaming server messages.

               For the `stream_pricing()` request, each server response message will be
               decoded as a `StreamPricing200Response` object. This object will contain
               information about ask and bid prices for the requested endpoints.

               The callback should be either a synchronous or asynchronous callable, such
               that will will receive each succesful sucessive `StreamPricing200Response`
               object.

               If callback_heartbeat is True, the callback will also receive decoded server
               heartbeat messages of a type `PricingHeartbeat`

        :param callback_heartbeat: If True, the callback will receive an ApiObject for each
               streaming heartbeat message. By default, streaming heatbeat messages will be
               skipped by the JSON decoder process.

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :param instruments: List of Instruments to stream Prices for. (required)
        :type instruments: List[str]
        :param snapshot: Flag that enables/disables the sending of a pricing snapshot when initially connecting to the stream.
        :type snapshot: bool

        :return: TBD
        :rtype: TBD

        Exceptions: TBD
        """

        assert len(instruments) is not int(0), "No instruments provided in request" # nosec B101

        _path_params = {'accountID': account_id}

        _query_params: dict[str, Any] = {'instruments': instruments}
        _collection_formats = {'instruments': 'csv'}

        if snapshot:
            _query_params['snapshot'] = snapshot

        _response_types_map = {
            0: models.PricingHeartbeat,
            200: models.StreamPricing200Response
        }

        types_callback = self.__class__.get_streaming_type_callback(_response_types_map, callback_heartbeat)
        receiver = ModelBuilder.from_receiver_gen(types_callback, model_callback)

        return await self.api_client.call_api(
            '/accounts/{accountID}/pricing/stream', RequestMethod.GET,
            path_params=_path_params,
            query_params=_query_params,
            collection_formats=_collection_formats,
            streaming=True, receiver=receiver,
            future=future)

    @validate_request
    async def stream_transactions(self,
                                  callback: Union[CoroutineType, FunctionType],
                                  account_id: AccountId,
                                  future: Optional[aio.Future[Literal[True]]] = None
                                  ) -> Awaitable[StreamTransactions200Response]:
        """Transaction Stream

        Get a stream of Transactions for an Account starting from when the request is made.

        >>> response = api.stream_transactions(account_id)

        :param account_id: Account Identifier (required)
        :type account_id: AccountId
        :return: Returns the response object.
        :rtype: tuple(StreamTransactions200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _path_params = {'accountID': account_id}

        _response_types_map = {
            0: models.TransactionHeartbeat,
            200: models.StreamTransactions200Response
        }

        types_callback = self.__class__.get_streaming_type_callback(_response_types_map)

        receiver = ModelBuilder.from_receiver_gen(types_callback, callback)

        return await self.api_client.call_api(
            '/accounts/{accountID}/transactions/stream', RequestMethod.GET,
            path_params=_path_params, streaming=True, receiver=receiver,
            future=future)


__all__ = exporting(__name__, ...)
