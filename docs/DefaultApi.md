# pyfx.dispatch.oanda.DefaultApi

All URIs are relative to */v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cancel_order**](DefaultApi.md#cancel_order) | **PUT** /accounts/{accountID}/orders/{orderSpecifier}/cancel | Cancel Order
[**close_position**](DefaultApi.md#close_position) | **PUT** /accounts/{accountID}/positions/{instrument}/close | Close Position
[**close_trade**](DefaultApi.md#close_trade) | **PUT** /accounts/{accountID}/trades/{tradeSpecifier}/close | Close Trade
[**configure_account**](DefaultApi.md#configure_account) | **PATCH** /accounts/{accountID}/configuration | Configure Account
[**create_order**](DefaultApi.md#create_order) | **POST** /accounts/{accountID}/orders | Create Order
[**get_account**](DefaultApi.md#get_account) | **GET** /accounts/{accountID} | Account Details
[**get_account_changes**](DefaultApi.md#get_account_changes) | **GET** /accounts/{accountID}/changes | Poll Account Updates
[**get_account_instruments**](DefaultApi.md#get_account_instruments) | **GET** /accounts/{accountID}/instruments | Account Instruments
[**get_account_summary**](DefaultApi.md#get_account_summary) | **GET** /accounts/{accountID}/summary | Account Summary
[**get_base_prices**](DefaultApi.md#get_base_prices) | **GET** /pricing | Get Base Prices
[**get_external_user_info**](DefaultApi.md#get_external_user_info) | **GET** /users/{userSpecifier}/externalInfo | External User Info
[**get_instrument_candles**](DefaultApi.md#get_instrument_candles) | **GET** /instruments/{instrument}/candles | Get Candlesticks
[**get_instrument_candles_0**](DefaultApi.md#get_instrument_candles_0) | **GET** /accounts/{accountID}/instruments/{instrument}/candles | Get Candlesticks
[**get_instrument_price**](DefaultApi.md#get_instrument_price) | **GET** /instruments/{instrument}/price | Price
[**get_instrument_price_range**](DefaultApi.md#get_instrument_price_range) | **GET** /instruments/{instrument}/price/range | Get Prices
[**get_order**](DefaultApi.md#get_order) | **GET** /accounts/{accountID}/orders/{orderSpecifier} | Get Order
[**get_position**](DefaultApi.md#get_position) | **GET** /accounts/{accountID}/positions/{instrument} | Instrument Position
[**get_price_range**](DefaultApi.md#get_price_range) | **GET** /pricing/range | Get Price Range
[**get_prices**](DefaultApi.md#get_prices) | **GET** /accounts/{accountID}/pricing | Current Account Prices
[**get_trade**](DefaultApi.md#get_trade) | **GET** /accounts/{accountID}/trades/{tradeSpecifier} | Trade Details
[**get_transaction**](DefaultApi.md#get_transaction) | **GET** /accounts/{accountID}/transactions/{transactionID} | Transaction Details
[**get_transaction_range**](DefaultApi.md#get_transaction_range) | **GET** /accounts/{accountID}/transactions/idrange | Transaction ID Range
[**get_transactions_since_id**](DefaultApi.md#get_transactions_since_id) | **GET** /accounts/{accountID}/transactions/sinceid | Transactions Since ID
[**get_user_info**](DefaultApi.md#get_user_info) | **GET** /users/{userSpecifier} | User Info
[**instruments_instrument_order_book_get**](DefaultApi.md#instruments_instrument_order_book_get) | **GET** /instruments/{instrument}/orderBook | Get Order Book
[**instruments_instrument_position_book_get**](DefaultApi.md#instruments_instrument_position_book_get) | **GET** /instruments/{instrument}/positionBook | Get Position Book
[**list_accounts**](DefaultApi.md#list_accounts) | **GET** /accounts | List Accounts
[**list_open_positions**](DefaultApi.md#list_open_positions) | **GET** /accounts/{accountID}/openPositions | Open Positions
[**list_open_trades**](DefaultApi.md#list_open_trades) | **GET** /accounts/{accountID}/openTrades | List Open Trades
[**list_orders**](DefaultApi.md#list_orders) | **GET** /accounts/{accountID}/orders | List Orders
[**list_pending_orders**](DefaultApi.md#list_pending_orders) | **GET** /accounts/{accountID}/pendingOrders | Pending Orders
[**list_positions**](DefaultApi.md#list_positions) | **GET** /accounts/{accountID}/positions | List Positions
[**list_trades**](DefaultApi.md#list_trades) | **GET** /accounts/{accountID}/trades | List Trades
[**list_transactions**](DefaultApi.md#list_transactions) | **GET** /accounts/{accountID}/transactions | List Transactions
[**replace_order**](DefaultApi.md#replace_order) | **PUT** /accounts/{accountID}/orders/{orderSpecifier} | Replace Order
[**set_order_client_extensions**](DefaultApi.md#set_order_client_extensions) | **PUT** /accounts/{accountID}/orders/{orderSpecifier}/clientExtensions | Set Order Extensions
[**set_trade_client_extensions**](DefaultApi.md#set_trade_client_extensions) | **PUT** /accounts/{accountID}/trades/{tradeSpecifier}/clientExtensions | Set Trade Client Extensions
[**set_trade_dependent_orders**](DefaultApi.md#set_trade_dependent_orders) | **PUT** /accounts/{accountID}/trades/{tradeSpecifier}/orders | Set Dependent Orders
[**stream_pricing**](DefaultApi.md#stream_pricing) | **GET** /accounts/{accountID}/pricing/stream | Price Stream
[**stream_transactions**](DefaultApi.md#stream_transactions) | **GET** /accounts/{accountID}/transactions/stream | Transaction Stream


# **cancel_order**
> CancelOrder200Response cancel_order(authorization, account_id, order_specifier, accept_datetime_format=accept_datetime_format, client_request_id=client_request_id)

Cancel Order

Cancel a pending Order in an Account

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.cancel_order200_response import CancelOrder200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    order_specifier = 'order_specifier_example' # str | The Order Specifier
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    client_request_id = 'client_request_id_example' # str | Client specified RequestID to be sent with request. (optional)

    try:
        # Cancel Order
        api_response = await api_instance.cancel_order(authorization, account_id, order_specifier, accept_datetime_format=accept_datetime_format, client_request_id=client_request_id)
        print("The response of DefaultApi->cancel_order:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->cancel_order: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **order_specifier** | **str**| The Order Specifier | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **client_request_id** | **str**| Client specified RequestID to be sent with request. | [optional] 

### Return type

[**CancelOrder200Response**](CancelOrder200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Order was cancelled as specified |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | The Account or Order specified does not exist. |  -  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **close_position**
> ClosePosition200Response close_position(authorization, account_id, instrument, close_position_body, accept_datetime_format=accept_datetime_format)

Close Position

Closeout the open Position for a specific instrument in an Account.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.close_position200_response import ClosePosition200Response
from pyfx.dispatch.oanda.models.close_position_request import ClosePositionRequest
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    instrument = 'instrument_example' # str | Name of the Instrument
    close_position_body = pyfx.dispatch.oanda.ClosePositionRequest() # ClosePositionRequest | Representation of how to close the position
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)

    try:
        # Close Position
        api_response = await api_instance.close_position(authorization, account_id, instrument, close_position_body, accept_datetime_format=accept_datetime_format)
        print("The response of DefaultApi->close_position:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->close_position: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **instrument** | **str**| Name of the Instrument | 
 **close_position_body** | [**ClosePositionRequest**](ClosePositionRequest.md)| Representation of how to close the position | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 

### Return type

[**ClosePosition200Response**](ClosePosition200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Position closeout request has been successfully processed. |  * RequestID - The unique identifier generated for the request <br>  * Location - A link to the replacing Order <br>  |
**400** | The Parameters provided that describe the Position closeout are invalid. |  -  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | The Account or one or more of the Positions specified does not exist. |  -  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **close_trade**
> CloseTrade200Response close_trade(authorization, account_id, trade_specifier, close_trade_body, accept_datetime_format=accept_datetime_format)

Close Trade

Close (partially or fully) a specific open Trade in an Account

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.close_trade200_response import CloseTrade200Response
from pyfx.dispatch.oanda.models.close_trade_request import CloseTradeRequest
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    trade_specifier = 'trade_specifier_example' # str | Specifier for the Trade
    close_trade_body = pyfx.dispatch.oanda.CloseTradeRequest() # CloseTradeRequest | Details of how much of the open Trade to close.
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)

    try:
        # Close Trade
        api_response = await api_instance.close_trade(authorization, account_id, trade_specifier, close_trade_body, accept_datetime_format=accept_datetime_format)
        print("The response of DefaultApi->close_trade:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->close_trade: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **trade_specifier** | **str**| Specifier for the Trade | 
 **close_trade_body** | [**CloseTradeRequest**](CloseTradeRequest.md)| Details of how much of the open Trade to close. | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 

### Return type

[**CloseTrade200Response**](CloseTrade200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Trade has been closed as requested |  * RequestID - The unique identifier generated for the request <br>  |
**400** | The Trade cannot be closed as requested. |  -  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | The Account or Trade specified does not exist. |  -  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **configure_account**
> ConfigureAccount200Response configure_account(authorization, account_id, accept_datetime_format=accept_datetime_format, configure_account_body=configure_account_body)

Configure Account

Set the client-configurable portions of an Account.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.configure_account200_response import ConfigureAccount200Response
from pyfx.dispatch.oanda.models.configure_account_request import ConfigureAccountRequest
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    configure_account_body = pyfx.dispatch.oanda.ConfigureAccountRequest() # ConfigureAccountRequest | Representation of the Account configuration to set (optional)

    try:
        # Configure Account
        api_response = await api_instance.configure_account(authorization, account_id, accept_datetime_format=accept_datetime_format, configure_account_body=configure_account_body)
        print("The response of DefaultApi->configure_account:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->configure_account: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **configure_account_body** | [**ConfigureAccountRequest**](ConfigureAccountRequest.md)| Representation of the Account configuration to set | [optional] 

### Return type

[**ConfigureAccount200Response**](ConfigureAccount200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Account was configured successfully. |  * RequestID - The unique identifier generated for the request <br>  |
**400** | The configuration specification was invalid. |  -  |
**403** | The configuration operation was forbidden on the Account. |  -  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_order**
> CreateOrder201Response create_order(authorization, account_id, create_order_body, accept_datetime_format=accept_datetime_format)

Create Order

Create an Order for an Account

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.create_order201_response import CreateOrder201Response
from pyfx.dispatch.oanda.models.create_order_request import CreateOrderRequest
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    create_order_body = pyfx.dispatch.oanda.CreateOrderRequest() # CreateOrderRequest | 
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)

    try:
        # Create Order
        api_response = await api_instance.create_order(authorization, account_id, create_order_body, accept_datetime_format=accept_datetime_format)
        print("The response of DefaultApi->create_order:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->create_order: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **create_order_body** | [**CreateOrderRequest**](CreateOrderRequest.md)|  | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 

### Return type

[**CreateOrder201Response**](CreateOrder201Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The Order was created as specified |  * RequestID - The unique identifier generated for the request <br>  * Location - A link to the replacing Order <br>  |
**400** | The Order specification was invalid |  -  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**403** | Forbidden. The client has provided a token that does not authorize them to perform the action implemented by the API endpoint. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | The Order or Account specified does not exist. |  -  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_account**
> GetAccount200Response get_account(authorization, account_id, accept_datetime_format=accept_datetime_format)

Account Details

Get the full details for a single Account that a client has access to. Full pending Order, open Trade and open Position representations are provided.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_account200_response import GetAccount200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)

    try:
        # Account Details
        api_response = await api_instance.get_account(authorization, account_id, accept_datetime_format=accept_datetime_format)
        print("The response of DefaultApi->get_account:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_account: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 

### Return type

[**GetAccount200Response**](GetAccount200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The full Account details are provided |  * RequestID - The unique identifier generated for the request <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_account_changes**
> GetAccountChanges200Response get_account_changes(authorization, account_id, accept_datetime_format=accept_datetime_format, since_transaction_id=since_transaction_id)

Poll Account Updates

Endpoint used to poll an Account for its current state and changes since a specified TransactionID.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_account_changes200_response import GetAccountChanges200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    since_transaction_id = 'since_transaction_id_example' # str | ID of the Transaction to get Account changes since. (optional)

    try:
        # Poll Account Updates
        api_response = await api_instance.get_account_changes(authorization, account_id, accept_datetime_format=accept_datetime_format, since_transaction_id=since_transaction_id)
        print("The response of DefaultApi->get_account_changes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_account_changes: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **since_transaction_id** | **str**| ID of the Transaction to get Account changes since. | [optional] 

### Return type

[**GetAccountChanges200Response**](GetAccountChanges200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Account state and changes are provided. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |
**416** | Range Not Satisfiable. The client has specified a range that is invalid or cannot be processed. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_account_instruments**
> GetAccountInstruments200Response get_account_instruments(authorization, account_id, instruments=instruments)

Account Instruments

Get the list of tradeable instruments for the given Account. The list of tradeable instruments is dependent on the regulatory division that the Account is located in, thus should be the same for all Accounts owned by a single user.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_account_instruments200_response import GetAccountInstruments200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    instruments = ['instruments_example'] # List[str] | List of instruments to query specifically. (optional)

    try:
        # Account Instruments
        api_response = await api_instance.get_account_instruments(authorization, account_id, instruments=instruments)
        print("The response of DefaultApi->get_account_instruments:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_account_instruments: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **instruments** | [**List[str]**](str.md)| List of instruments to query specifically. | [optional] 

### Return type

[**GetAccountInstruments200Response**](GetAccountInstruments200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of tradeable instruments for the Account has been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_account_summary**
> GetAccountSummary200Response get_account_summary(authorization, account_id, accept_datetime_format=accept_datetime_format)

Account Summary

Get a summary for a single Account that a client has access to.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_account_summary200_response import GetAccountSummary200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)

    try:
        # Account Summary
        api_response = await api_instance.get_account_summary(authorization, account_id, accept_datetime_format=accept_datetime_format)
        print("The response of DefaultApi->get_account_summary:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_account_summary: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 

### Return type

[**GetAccountSummary200Response**](GetAccountSummary200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Account summary  are provided |  * RequestID - The unique identifier generated for the request <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_base_prices**
> GetInstrumentPriceRange200Response get_base_prices(authorization, accept_datetime_format=accept_datetime_format, time=time)

Get Base Prices

Get pricing information for a specified instrument. Accounts are not associated in any way with this endpoint.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_instrument_price_range200_response import GetInstrumentPriceRange200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    time = 'time_example' # str | The time at which the desired price for each instrument is in effect. The current price for each instrument is returned if no time is provided. (optional)

    try:
        # Get Base Prices
        api_response = await api_instance.get_base_prices(authorization, accept_datetime_format=accept_datetime_format, time=time)
        print("The response of DefaultApi->get_base_prices:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_base_prices: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **time** | **str**| The time at which the desired price for each instrument is in effect. The current price for each instrument is returned if no time is provided. | [optional] 

### Return type

[**GetInstrumentPriceRange200Response**](GetInstrumentPriceRange200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Pricing information has been successfully provided. |  * RequestID - The unique identifier generated for the request <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_external_user_info**
> GetExternalUserInfo200Response get_external_user_info(authorization, user_specifier)

External User Info

Fetch the externally-available user information for the specified user. This endpoint is intended to be used by 3rd parties that have been authorized by a user to view their personal information.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_external_user_info200_response import GetExternalUserInfo200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    user_specifier = 'user_specifier_example' # str | The User Specifier

    try:
        # External User Info
        api_response = await api_instance.get_external_user_info(authorization, user_specifier)
        print("The response of DefaultApi->get_external_user_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_external_user_info: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **user_specifier** | **str**| The User Specifier | 

### Return type

[**GetExternalUserInfo200Response**](GetExternalUserInfo200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The external user information has been provided |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**403** | Forbidden. The client has provided a token that does not authorize them to perform the action implemented by the API endpoint. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_instrument_candles**
> GetInstrumentCandles200Response get_instrument_candles(authorization, instrument, accept_datetime_format=accept_datetime_format, price=price, granularity=granularity, count=count, var_from=var_from, to=to, smooth=smooth, include_first=include_first, daily_alignment=daily_alignment, alignment_timezone=alignment_timezone, weekly_alignment=weekly_alignment)

Get Candlesticks

Fetch candlestick data for an instrument.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_instrument_candles200_response import GetInstrumentCandles200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    instrument = 'instrument_example' # str | Name of the Instrument
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    price = 'price_example' # str | The Price component(s) to get candlestick data for. Can contain any combination of the characters \"M\" (midpoint candles) \"B\" (bid candles) and \"A\" (ask candles). (optional)
    granularity = 'granularity_example' # str | The granularity of the candlesticks to fetch (optional)
    count = 56 # int | The number of candlesticks to return in the reponse. Count should not be specified if both the start and end parameters are provided, as the time range combined with the graularity will determine the number of candlesticks to return. (optional)
    var_from = 'var_from_example' # str | The start of the time range to fetch candlesticks for. (optional)
    to = 'to_example' # str | The end of the time range to fetch candlesticks for. (optional)
    smooth = True # bool | A flag that controls whether the candlestick is \"smoothed\" or not.  A smoothed candlestick uses the previous candle's close price as its open price, while an unsmoothed candlestick uses the first price from its time range as its open price. (optional)
    include_first = True # bool | A flag that controls whether the candlestick that is covered by the from time should be included in the results. This flag enables clients to use the timestamp of the last completed candlestick received to poll for future candlesticks but avoid receiving the previous candlestick repeatedly. (optional)
    daily_alignment = 56 # int | The hour of the day (in the specified timezone) to use for granularities that have daily alignments. (optional)
    alignment_timezone = 'alignment_timezone_example' # str | The timezone to use for the dailyAlignment parameter. Candlesticks with daily alignment will be aligned to the dailyAlignment hour within the alignmentTimezone.  Note that the returned times will still be represented in UTC. (optional)
    weekly_alignment = 'weekly_alignment_example' # str | The day of the week used for granularities that have weekly alignment. (optional)

    try:
        # Get Candlesticks
        api_response = await api_instance.get_instrument_candles(authorization, instrument, accept_datetime_format=accept_datetime_format, price=price, granularity=granularity, count=count, var_from=var_from, to=to, smooth=smooth, include_first=include_first, daily_alignment=daily_alignment, alignment_timezone=alignment_timezone, weekly_alignment=weekly_alignment)
        print("The response of DefaultApi->get_instrument_candles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_instrument_candles: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **instrument** | **str**| Name of the Instrument | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **price** | **str**| The Price component(s) to get candlestick data for. Can contain any combination of the characters \&quot;M\&quot; (midpoint candles) \&quot;B\&quot; (bid candles) and \&quot;A\&quot; (ask candles). | [optional] 
 **granularity** | **str**| The granularity of the candlesticks to fetch | [optional] 
 **count** | **int**| The number of candlesticks to return in the reponse. Count should not be specified if both the start and end parameters are provided, as the time range combined with the graularity will determine the number of candlesticks to return. | [optional] 
 **var_from** | **str**| The start of the time range to fetch candlesticks for. | [optional] 
 **to** | **str**| The end of the time range to fetch candlesticks for. | [optional] 
 **smooth** | **bool**| A flag that controls whether the candlestick is \&quot;smoothed\&quot; or not.  A smoothed candlestick uses the previous candle&#39;s close price as its open price, while an unsmoothed candlestick uses the first price from its time range as its open price. | [optional] 
 **include_first** | **bool**| A flag that controls whether the candlestick that is covered by the from time should be included in the results. This flag enables clients to use the timestamp of the last completed candlestick received to poll for future candlesticks but avoid receiving the previous candlestick repeatedly. | [optional] 
 **daily_alignment** | **int**| The hour of the day (in the specified timezone) to use for granularities that have daily alignments. | [optional] 
 **alignment_timezone** | **str**| The timezone to use for the dailyAlignment parameter. Candlesticks with daily alignment will be aligned to the dailyAlignment hour within the alignmentTimezone.  Note that the returned times will still be represented in UTC. | [optional] 
 **weekly_alignment** | **str**| The day of the week used for granularities that have weekly alignment. | [optional] 

### Return type

[**GetInstrumentCandles200Response**](GetInstrumentCandles200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Pricing information has been successfully provided. |  * RequestID - The unique identifier generated for the request <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_instrument_candles_0**
> GetInstrumentCandles200Response get_instrument_candles_0(authorization, instrument, accept_datetime_format=accept_datetime_format, price=price, granularity=granularity, count=count, var_from=var_from, to=to, smooth=smooth, include_first=include_first, daily_alignment=daily_alignment, alignment_timezone=alignment_timezone, weekly_alignment=weekly_alignment, units=units)

Get Candlesticks

Fetch candlestick data for an instrument.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_instrument_candles200_response import GetInstrumentCandles200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    instrument = 'instrument_example' # str | Name of the Instrument
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    price = 'price_example' # str | The Price component(s) to get candlestick data for. Can contain any combination of the characters \"M\" (midpoint candles) \"B\" (bid candles) and \"A\" (ask candles). (optional)
    granularity = 'granularity_example' # str | The granularity of the candlesticks to fetch (optional)
    count = 56 # int | The number of candlesticks to return in the response. Count should not be specified if both the start and end parameters are provided, as the time range combined with the granularity will determine the number of candlesticks to return. (optional)
    var_from = 'var_from_example' # str | The start of the time range to fetch candlesticks for. (optional)
    to = 'to_example' # str | The end of the time range to fetch candlesticks for. (optional)
    smooth = True # bool | A flag that controls whether the candlestick is \"smoothed\" or not.  A smoothed candlestick uses the previous candle's close price as its open price, while an unsmoothed candlestick uses the first price from its time range as its open price. (optional)
    include_first = True # bool | A flag that controls whether the candlestick that is covered by the from time should be included in the results. This flag enables clients to use the timestamp of the last completed candlestick received to poll for future candlesticks but avoid receiving the previous candlestick repeatedly. (optional)
    daily_alignment = 56 # int | The hour of the day (in the specified timezone) to use for granularities that have daily alignments. (optional)
    alignment_timezone = 'alignment_timezone_example' # str | The timezone to use for the dailyAlignment parameter. Candlesticks with daily alignment will be aligned to the dailyAlignment hour within the alignmentTimezone.  Note that the returned times will still be represented in UTC. (optional)
    weekly_alignment = 'weekly_alignment_example' # str | The day of the week used for granularities that have weekly alignment. (optional)
    units = 'units_example' # str | The number of units used to calculate the volume-weighted average bid and ask prices in the returned candles. (optional)

    try:
        # Get Candlesticks
        api_response = await api_instance.get_instrument_candles_0(authorization, instrument, accept_datetime_format=accept_datetime_format, price=price, granularity=granularity, count=count, var_from=var_from, to=to, smooth=smooth, include_first=include_first, daily_alignment=daily_alignment, alignment_timezone=alignment_timezone, weekly_alignment=weekly_alignment, units=units)
        print("The response of DefaultApi->get_instrument_candles_0:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_instrument_candles_0: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **instrument** | **str**| Name of the Instrument | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **price** | **str**| The Price component(s) to get candlestick data for. Can contain any combination of the characters \&quot;M\&quot; (midpoint candles) \&quot;B\&quot; (bid candles) and \&quot;A\&quot; (ask candles). | [optional] 
 **granularity** | **str**| The granularity of the candlesticks to fetch | [optional] 
 **count** | **int**| The number of candlesticks to return in the response. Count should not be specified if both the start and end parameters are provided, as the time range combined with the granularity will determine the number of candlesticks to return. | [optional] 
 **var_from** | **str**| The start of the time range to fetch candlesticks for. | [optional] 
 **to** | **str**| The end of the time range to fetch candlesticks for. | [optional] 
 **smooth** | **bool**| A flag that controls whether the candlestick is \&quot;smoothed\&quot; or not.  A smoothed candlestick uses the previous candle&#39;s close price as its open price, while an unsmoothed candlestick uses the first price from its time range as its open price. | [optional] 
 **include_first** | **bool**| A flag that controls whether the candlestick that is covered by the from time should be included in the results. This flag enables clients to use the timestamp of the last completed candlestick received to poll for future candlesticks but avoid receiving the previous candlestick repeatedly. | [optional] 
 **daily_alignment** | **int**| The hour of the day (in the specified timezone) to use for granularities that have daily alignments. | [optional] 
 **alignment_timezone** | **str**| The timezone to use for the dailyAlignment parameter. Candlesticks with daily alignment will be aligned to the dailyAlignment hour within the alignmentTimezone.  Note that the returned times will still be represented in UTC. | [optional] 
 **weekly_alignment** | **str**| The day of the week used for granularities that have weekly alignment. | [optional] 
 **units** | **str**| The number of units used to calculate the volume-weighted average bid and ask prices in the returned candles. | [optional] 

### Return type

[**GetInstrumentCandles200Response**](GetInstrumentCandles200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Pricing information has been successfully provided. |  * RequestID - The unique identifier generated for the request <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_instrument_price**
> GetInstrumentPrice200Response get_instrument_price(authorization, instrument, accept_datetime_format=accept_datetime_format, time=time)

Price

Fetch a price for an instrument. Accounts are not associated in any way with this endpoint.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_instrument_price200_response import GetInstrumentPrice200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    instrument = 'instrument_example' # str | Name of the Instrument
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    time = 'time_example' # str | The time at which the desired price is in effect. The current price is returned if no time is provided. (optional)

    try:
        # Price
        api_response = await api_instance.get_instrument_price(authorization, instrument, accept_datetime_format=accept_datetime_format, time=time)
        print("The response of DefaultApi->get_instrument_price:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_instrument_price: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **instrument** | **str**| Name of the Instrument | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **time** | **str**| The time at which the desired price is in effect. The current price is returned if no time is provided. | [optional] 

### Return type

[**GetInstrumentPrice200Response**](GetInstrumentPrice200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Pricing information has been successfully provided. |  * RequestID - The unique identifier generated for the request <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_instrument_price_range**
> GetInstrumentPriceRange200Response get_instrument_price_range(authorization, instrument, var_from, accept_datetime_format=accept_datetime_format, to=to)

Get Prices

Fetch a range of prices for an instrument. Accounts are not associated in any way with this endpoint.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_instrument_price_range200_response import GetInstrumentPriceRange200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    instrument = 'instrument_example' # str | Name of the Instrument
    var_from = 'var_from_example' # str | The start of the time range to fetch prices for.
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    to = 'to_example' # str | The end of the time range to fetch prices for. The current time is used if this parameter is not provided. (optional)

    try:
        # Get Prices
        api_response = await api_instance.get_instrument_price_range(authorization, instrument, var_from, accept_datetime_format=accept_datetime_format, to=to)
        print("The response of DefaultApi->get_instrument_price_range:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_instrument_price_range: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **instrument** | **str**| Name of the Instrument | 
 **var_from** | **str**| The start of the time range to fetch prices for. | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **to** | **str**| The end of the time range to fetch prices for. The current time is used if this parameter is not provided. | [optional] 

### Return type

[**GetInstrumentPriceRange200Response**](GetInstrumentPriceRange200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Pricing information has been successfully provided. |  * RequestID - The unique identifier generated for the request <br>  * Link - A link to the next page of results if the results were paginated <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_order**
> GetOrder200Response get_order(authorization, account_id, order_specifier, accept_datetime_format=accept_datetime_format)

Get Order

Get details for a single Order in an Account

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_order200_response import GetOrder200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    order_specifier = 'order_specifier_example' # str | The Order Specifier
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)

    try:
        # Get Order
        api_response = await api_instance.get_order(authorization, account_id, order_specifier, accept_datetime_format=accept_datetime_format)
        print("The response of DefaultApi->get_order:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_order: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **order_specifier** | **str**| The Order Specifier | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 

### Return type

[**GetOrder200Response**](GetOrder200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The details of the Order requested |  * RequestID - The unique identifier generated for the request <br>  * Link - A link to the next page of results if the results were paginated <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_position**
> GetPosition200Response get_position(authorization, account_id, instrument)

Instrument Position

Get the details of a single Instrument's Position in an Account. The Position may by open or not.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_position200_response import GetPosition200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    instrument = 'instrument_example' # str | Name of the Instrument

    try:
        # Instrument Position
        api_response = await api_instance.get_position(authorization, account_id, instrument)
        print("The response of DefaultApi->get_position:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_position: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **instrument** | **str**| Name of the Instrument | 

### Return type

[**GetPosition200Response**](GetPosition200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Position is provided. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_price_range**
> GetInstrumentPriceRange200Response get_price_range(authorization, instrument, var_from, accept_datetime_format=accept_datetime_format, to=to)

Get Price Range

Get pricing information for a specified range of prices. Accounts are not associated in any way with this endpoint.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_instrument_price_range200_response import GetInstrumentPriceRange200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    instrument = 'instrument_example' # str | Name of the Instrument
    var_from = 'var_from_example' # str | The start of the time range to fetch prices for.
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    to = 'to_example' # str | The end of the time range to fetch prices for. The current time is used if this parameter is not provided. (optional)

    try:
        # Get Price Range
        api_response = await api_instance.get_price_range(authorization, instrument, var_from, accept_datetime_format=accept_datetime_format, to=to)
        print("The response of DefaultApi->get_price_range:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_price_range: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **instrument** | **str**| Name of the Instrument | 
 **var_from** | **str**| The start of the time range to fetch prices for. | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **to** | **str**| The end of the time range to fetch prices for. The current time is used if this parameter is not provided. | [optional] 

### Return type

[**GetInstrumentPriceRange200Response**](GetInstrumentPriceRange200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Pricing information has been successfully provided. |  * RequestID - The unique identifier generated for the request <br>  * Link - A link to the next page of results if the results were paginated <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_prices**
> GetPrices200Response get_prices(authorization, account_id, instruments, accept_datetime_format=accept_datetime_format, since=since, include_units_available=include_units_available, include_home_conversions=include_home_conversions)

Current Account Prices

Get pricing information for a specified list of Instruments within an Account.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_prices200_response import GetPrices200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    instruments = ['instruments_example'] # List[str] | List of Instruments to get pricing for.
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    since = 'since_example' # str | Date/Time filter to apply to the response. Only prices and home conversions (if requested) with a time later than this filter (i.e. the price has changed after the since time) will be provided, and are filtered independently. (optional)
    include_units_available = True # bool | Flag that enables the inclusion of the unitsAvailable field in the returned Price objects. (optional)
    include_home_conversions = True # bool | Flag that enables the inclusion of the homeConversions field in the returned response. An entry will be returned for each currency in the set of all base and quote currencies present in the requested instruments list. (optional)

    try:
        # Current Account Prices
        api_response = await api_instance.get_prices(authorization, account_id, instruments, accept_datetime_format=accept_datetime_format, since=since, include_units_available=include_units_available, include_home_conversions=include_home_conversions)
        print("The response of DefaultApi->get_prices:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_prices: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **instruments** | [**List[str]**](str.md)| List of Instruments to get pricing for. | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **since** | **str**| Date/Time filter to apply to the response. Only prices and home conversions (if requested) with a time later than this filter (i.e. the price has changed after the since time) will be provided, and are filtered independently. | [optional] 
 **include_units_available** | **bool**| Flag that enables the inclusion of the unitsAvailable field in the returned Price objects. | [optional] 
 **include_home_conversions** | **bool**| Flag that enables the inclusion of the homeConversions field in the returned response. An entry will be returned for each currency in the set of all base and quote currencies present in the requested instruments list. | [optional] 

### Return type

[**GetPrices200Response**](GetPrices200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Pricing information has been successfully provided. |  * RequestID - The unique identifier generated for the request <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trade**
> GetTrade200Response get_trade(authorization, account_id, trade_specifier, accept_datetime_format=accept_datetime_format)

Trade Details

Get the details of a specific Trade in an Account

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_trade200_response import GetTrade200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    trade_specifier = 'trade_specifier_example' # str | Specifier for the Trade
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)

    try:
        # Trade Details
        api_response = await api_instance.get_trade(authorization, account_id, trade_specifier, accept_datetime_format=accept_datetime_format)
        print("The response of DefaultApi->get_trade:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_trade: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **trade_specifier** | **str**| Specifier for the Trade | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 

### Return type

[**GetTrade200Response**](GetTrade200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The details for the requested Trade is provided |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_transaction**
> GetTransaction200Response get_transaction(authorization, account_id, transaction_id, accept_datetime_format=accept_datetime_format)

Transaction Details

Get the details of a single Account Transaction.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_transaction200_response import GetTransaction200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    transaction_id = 'transaction_id_example' # str | A Transaction ID
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)

    try:
        # Transaction Details
        api_response = await api_instance.get_transaction(authorization, account_id, transaction_id, accept_datetime_format=accept_datetime_format)
        print("The response of DefaultApi->get_transaction:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_transaction: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **transaction_id** | **str**| A Transaction ID | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 

### Return type

[**GetTransaction200Response**](GetTransaction200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The details of the requested Transaction are provided. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_transaction_range**
> GetTransactionRange200Response get_transaction_range(authorization, account_id, var_from, to, accept_datetime_format=accept_datetime_format, type=type)

Transaction ID Range

Get a range of Transactions for an Account based on the Transaction IDs.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_transaction_range200_response import GetTransactionRange200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    var_from = 'var_from_example' # str | The starting Transacion ID (inclusive) to fetch.
    to = 'to_example' # str | The ending Transaction ID (inclusive) to fetch.
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    type = ['type_example'] # List[str] | The filter that restricts the types of Transactions to retreive. (optional)

    try:
        # Transaction ID Range
        api_response = await api_instance.get_transaction_range(authorization, account_id, var_from, to, accept_datetime_format=accept_datetime_format, type=type)
        print("The response of DefaultApi->get_transaction_range:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_transaction_range: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **var_from** | **str**| The starting Transacion ID (inclusive) to fetch. | 
 **to** | **str**| The ending Transaction ID (inclusive) to fetch. | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **type** | [**List[str]**](str.md)| The filter that restricts the types of Transactions to retreive. | [optional] 

### Return type

[**GetTransactionRange200Response**](GetTransactionRange200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The requested time range of Transactions are provided. |  * RequestID - The unique identifier generated for the request <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |
**416** | Range Not Satisfiable. The client has specified a range that is invalid or cannot be processed. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_transactions_since_id**
> GetTransactionRange200Response get_transactions_since_id(authorization, account_id, id, accept_datetime_format=accept_datetime_format)

Transactions Since ID

Get a range of Transactions for an Account starting at (but not including) a provided Transaction ID.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_transaction_range200_response import GetTransactionRange200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    id = 'id_example' # str | The ID of the last Transacion fetched. This query will return all Transactions newer than the TransactionID.
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)

    try:
        # Transactions Since ID
        api_response = await api_instance.get_transactions_since_id(authorization, account_id, id, accept_datetime_format=accept_datetime_format)
        print("The response of DefaultApi->get_transactions_since_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_transactions_since_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **id** | **str**| The ID of the last Transacion fetched. This query will return all Transactions newer than the TransactionID. | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 

### Return type

[**GetTransactionRange200Response**](GetTransactionRange200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The requested time range of Transactions are provided. |  * RequestID - The unique identifier generated for the request <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |
**416** | Range Not Satisfiable. The client has specified a range that is invalid or cannot be processed. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_info**
> GetUserInfo200Response get_user_info(authorization, user_specifier)

User Info

Fetch the user information for the specified user. This endpoint is intended to be used by the user themself to obtain their own information.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.get_user_info200_response import GetUserInfo200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    user_specifier = 'user_specifier_example' # str | The User Specifier

    try:
        # User Info
        api_response = await api_instance.get_user_info(authorization, user_specifier)
        print("The response of DefaultApi->get_user_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_user_info: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **user_specifier** | **str**| The User Specifier | 

### Return type

[**GetUserInfo200Response**](GetUserInfo200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The user information has been provided |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**403** | Forbidden. The client has provided a token that does not authorize them to perform the action implemented by the API endpoint. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **instruments_instrument_order_book_get**
> InstrumentsInstrumentOrderBookGet200Response instruments_instrument_order_book_get(authorization, instrument, accept_datetime_format=accept_datetime_format, time=time)

Get Order Book

Fetch an order book for an instrument.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.instruments_instrument_order_book_get200_response import InstrumentsInstrumentOrderBookGet200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    instrument = 'instrument_example' # str | Name of the Instrument
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    time = 'time_example' # str | The time of the snapshot to fetch. If not specified, then the most recent snapshot is fetched. (optional)

    try:
        # Get Order Book
        api_response = await api_instance.instruments_instrument_order_book_get(authorization, instrument, accept_datetime_format=accept_datetime_format, time=time)
        print("The response of DefaultApi->instruments_instrument_order_book_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->instruments_instrument_order_book_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **instrument** | **str**| Name of the Instrument | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **time** | **str**| The time of the snapshot to fetch. If not specified, then the most recent snapshot is fetched. | [optional] 

### Return type

[**InstrumentsInstrumentOrderBookGet200Response**](InstrumentsInstrumentOrderBookGet200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The order book has been successfully provided. |  * RequestID - The unique identifier generated for the request <br>  * Content-Encoding - Value will be \&quot;gzip\&quot; regardless of provided Accept-Encoding header <br>  * Link - A link to the next page of results if the results were paginated <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **instruments_instrument_position_book_get**
> InstrumentsInstrumentPositionBookGet200Response instruments_instrument_position_book_get(authorization, instrument, accept_datetime_format=accept_datetime_format, time=time)

Get Position Book

Fetch a position book for an instrument.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.instruments_instrument_position_book_get200_response import InstrumentsInstrumentPositionBookGet200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    instrument = 'instrument_example' # str | Name of the Instrument
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    time = 'time_example' # str | The time of the snapshot to fetch. If not specified, then the most recent snapshot is fetched. (optional)

    try:
        # Get Position Book
        api_response = await api_instance.instruments_instrument_position_book_get(authorization, instrument, accept_datetime_format=accept_datetime_format, time=time)
        print("The response of DefaultApi->instruments_instrument_position_book_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->instruments_instrument_position_book_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **instrument** | **str**| Name of the Instrument | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **time** | **str**| The time of the snapshot to fetch. If not specified, then the most recent snapshot is fetched. | [optional] 

### Return type

[**InstrumentsInstrumentPositionBookGet200Response**](InstrumentsInstrumentPositionBookGet200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The position book has been successfully provided. |  * RequestID - The unique identifier generated for the request <br>  * Content-Encoding - Value will be \&quot;gzip\&quot; regardless of provided Accept-Encoding header <br>  * Link - A link to the next page of results if the results were paginated <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_accounts**
> ListAccounts200Response list_accounts(authorization)

List Accounts

Get a list of all Accounts authorized for the provided token.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.list_accounts200_response import ListAccounts200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client

    try:
        # List Accounts
        api_response = await api_instance.list_accounts(authorization)
        print("The response of DefaultApi->list_accounts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_accounts: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 

### Return type

[**ListAccounts200Response**](ListAccounts200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of authorized Accounts has been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_open_positions**
> ListOpenPositions200Response list_open_positions(authorization, account_id)

Open Positions

List all open Positions for an Account. An open Position is a Position in an Account that currently has a Trade opened for it.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.list_open_positions200_response import ListOpenPositions200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier

    try:
        # Open Positions
        api_response = await api_instance.list_open_positions(authorization, account_id)
        print("The response of DefaultApi->list_open_positions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_open_positions: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 

### Return type

[**ListOpenPositions200Response**](ListOpenPositions200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Account&#39;s open Positions are provided. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_open_trades**
> ListOpenTrades200Response list_open_trades(authorization, account_id, accept_datetime_format=accept_datetime_format)

List Open Trades

Get the list of open Trades for an Account

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.list_open_trades200_response import ListOpenTrades200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)

    try:
        # List Open Trades
        api_response = await api_instance.list_open_trades(authorization, account_id, accept_datetime_format=accept_datetime_format)
        print("The response of DefaultApi->list_open_trades:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_open_trades: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 

### Return type

[**ListOpenTrades200Response**](ListOpenTrades200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Account&#39;s list of open Trades is provided |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_orders**
> ListOrders200Response list_orders(authorization, account_id, accept_datetime_format=accept_datetime_format, ids=ids, state=state, instrument=instrument, count=count, before_id=before_id)

List Orders

Get a list of Orders for an Account

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.list_orders200_response import ListOrders200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    ids = ['ids_example'] # List[str] | List of Order IDs to retrieve (optional)
    state = 'state_example' # str | The state to filter the requested Orders by (optional)
    instrument = 'instrument_example' # str | The instrument to filter the requested orders by (optional)
    count = 56 # int | The maximum number of Orders to return (optional)
    before_id = 'before_id_example' # str | The maximum Order ID to return. If not provided the most recent Orders in the Account are returned (optional)

    try:
        # List Orders
        api_response = await api_instance.list_orders(authorization, account_id, accept_datetime_format=accept_datetime_format, ids=ids, state=state, instrument=instrument, count=count, before_id=before_id)
        print("The response of DefaultApi->list_orders:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_orders: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **ids** | [**List[str]**](str.md)| List of Order IDs to retrieve | [optional] 
 **state** | **str**| The state to filter the requested Orders by | [optional] 
 **instrument** | **str**| The instrument to filter the requested orders by | [optional] 
 **count** | **int**| The maximum number of Orders to return | [optional] 
 **before_id** | **str**| The maximum Order ID to return. If not provided the most recent Orders in the Account are returned | [optional] 

### Return type

[**ListOrders200Response**](ListOrders200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of Orders requested |  * RequestID - The unique identifier generated for the request <br>  * Link - A link to the next page of results if the results were paginated <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_pending_orders**
> ListPendingOrders200Response list_pending_orders(authorization, account_id, accept_datetime_format=accept_datetime_format)

Pending Orders

List all pending Orders in an Account

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.list_pending_orders200_response import ListPendingOrders200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)

    try:
        # Pending Orders
        api_response = await api_instance.list_pending_orders(authorization, account_id, accept_datetime_format=accept_datetime_format)
        print("The response of DefaultApi->list_pending_orders:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_pending_orders: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 

### Return type

[**ListPendingOrders200Response**](ListPendingOrders200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of pending Orders for the Account |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_positions**
> ListPositions200Response list_positions(authorization, account_id)

List Positions

List all Positions for an Account. The Positions returned are for every instrument that has had a position during the lifetime of an the Account.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.list_positions200_response import ListPositions200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier

    try:
        # List Positions
        api_response = await api_instance.list_positions(authorization, account_id)
        print("The response of DefaultApi->list_positions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_positions: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 

### Return type

[**ListPositions200Response**](ListPositions200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Account&#39;s Positions are provided. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_trades**
> ListTrades200Response list_trades(authorization, account_id, accept_datetime_format=accept_datetime_format, ids=ids, state=state, instrument=instrument, count=count, before_id=before_id)

List Trades

Get a list of Trades for an Account

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.list_trades200_response import ListTrades200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    ids = ['ids_example'] # List[str] | List of Trade IDs to retrieve. (optional)
    state = 'state_example' # str | The state to filter the requested Trades by. (optional)
    instrument = 'instrument_example' # str | The instrument to filter the requested Trades by. (optional)
    count = 56 # int | The maximum number of Trades to return. (optional)
    before_id = 'before_id_example' # str | The maximum Trade ID to return. If not provided the most recent Trades in the Account are returned. (optional)

    try:
        # List Trades
        api_response = await api_instance.list_trades(authorization, account_id, accept_datetime_format=accept_datetime_format, ids=ids, state=state, instrument=instrument, count=count, before_id=before_id)
        print("The response of DefaultApi->list_trades:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_trades: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **ids** | [**List[str]**](str.md)| List of Trade IDs to retrieve. | [optional] 
 **state** | **str**| The state to filter the requested Trades by. | [optional] 
 **instrument** | **str**| The instrument to filter the requested Trades by. | [optional] 
 **count** | **int**| The maximum number of Trades to return. | [optional] 
 **before_id** | **str**| The maximum Trade ID to return. If not provided the most recent Trades in the Account are returned. | [optional] 

### Return type

[**ListTrades200Response**](ListTrades200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of Trades requested |  * RequestID - The unique identifier generated for the request <br>  * Link - A link to the next page of results if the results were paginated <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_transactions**
> ListTransactions200Response list_transactions(authorization, account_id, accept_datetime_format=accept_datetime_format, var_from=var_from, to=to, page_size=page_size, type=type)

List Transactions

Get a list of Transactions pages that satisfy a time-based Transaction query.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.list_transactions200_response import ListTransactions200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    var_from = 'var_from_example' # str | The starting time (inclusive) of the time range for the Transactions being queried. (optional)
    to = 'to_example' # str | The ending time (inclusive) of the time range for the Transactions being queried. (optional)
    page_size = 56 # int | The number of Transactions to include in each page of the results. (optional)
    type = ['type_example'] # List[str] | A filter for restricting the types of Transactions to retreive. (optional)

    try:
        # List Transactions
        api_response = await api_instance.list_transactions(authorization, account_id, accept_datetime_format=accept_datetime_format, var_from=var_from, to=to, page_size=page_size, type=type)
        print("The response of DefaultApi->list_transactions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_transactions: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **var_from** | **str**| The starting time (inclusive) of the time range for the Transactions being queried. | [optional] 
 **to** | **str**| The ending time (inclusive) of the time range for the Transactions being queried. | [optional] 
 **page_size** | **int**| The number of Transactions to include in each page of the results. | [optional] 
 **type** | [**List[str]**](str.md)| A filter for restricting the types of Transactions to retreive. | [optional] 

### Return type

[**ListTransactions200Response**](ListTransactions200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The requested time range of Transaction pages are provided. |  * RequestID - The unique identifier generated for the request <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**403** | Forbidden. The client has provided a token that does not authorize them to perform the action implemented by the API endpoint. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |
**416** | Range Not Satisfiable. The client has specified a range that is invalid or cannot be processed. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_order**
> ReplaceOrder201Response replace_order(authorization, account_id, order_specifier, replace_order_body, accept_datetime_format=accept_datetime_format, client_request_id=client_request_id)

Replace Order

Replace an Order in an Account by simultaneously cancelling it and creating a replacement Order

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.create_order_request import CreateOrderRequest
from pyfx.dispatch.oanda.models.replace_order201_response import ReplaceOrder201Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    order_specifier = 'order_specifier_example' # str | The Order Specifier
    replace_order_body = pyfx.dispatch.oanda.CreateOrderRequest() # CreateOrderRequest | Specification of the replacing Order. The replacing order must have the same type as the replaced Order.
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    client_request_id = 'client_request_id_example' # str | Client specified RequestID to be sent with request. (optional)

    try:
        # Replace Order
        api_response = await api_instance.replace_order(authorization, account_id, order_specifier, replace_order_body, accept_datetime_format=accept_datetime_format, client_request_id=client_request_id)
        print("The response of DefaultApi->replace_order:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->replace_order: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **order_specifier** | **str**| The Order Specifier | 
 **replace_order_body** | [**CreateOrderRequest**](CreateOrderRequest.md)| Specification of the replacing Order. The replacing order must have the same type as the replaced Order. | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **client_request_id** | **str**| Client specified RequestID to be sent with request. | [optional] 

### Return type

[**ReplaceOrder201Response**](ReplaceOrder201Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The Order was successfully cancelled and replaced |  * RequestID - The unique identifier generated for the request <br>  * Location - A link to the replacing Order <br>  |
**400** | The Order specification was invalid |  -  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | The Account or Order specified does not exist. |  -  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_order_client_extensions**
> SetOrderClientExtensions200Response set_order_client_extensions(authorization, account_id, order_specifier, set_order_client_extensions_body, accept_datetime_format=accept_datetime_format)

Set Order Extensions

Update the Client Extensions for an Order in an Account. Do not set, modify, or delete clientExtensions if your account is associated with MT4.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.set_order_client_extensions200_response import SetOrderClientExtensions200Response
from pyfx.dispatch.oanda.models.set_order_client_extensions_request import SetOrderClientExtensionsRequest
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    order_specifier = 'order_specifier_example' # str | The Order Specifier
    set_order_client_extensions_body = pyfx.dispatch.oanda.SetOrderClientExtensionsRequest() # SetOrderClientExtensionsRequest | Representation of the replacing Order
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)

    try:
        # Set Order Extensions
        api_response = await api_instance.set_order_client_extensions(authorization, account_id, order_specifier, set_order_client_extensions_body, accept_datetime_format=accept_datetime_format)
        print("The response of DefaultApi->set_order_client_extensions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->set_order_client_extensions: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **order_specifier** | **str**| The Order Specifier | 
 **set_order_client_extensions_body** | [**SetOrderClientExtensionsRequest**](SetOrderClientExtensionsRequest.md)| Representation of the replacing Order | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 

### Return type

[**SetOrderClientExtensions200Response**](SetOrderClientExtensions200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Order&#39;s Client Extensions were successfully modified |  * RequestID - The unique identifier generated for the request <br>  |
**400** | The Order Client Extensions specification was invalid |  -  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | The Account or Order specified does not exist. |  -  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_trade_client_extensions**
> SetTradeClientExtensions200Response set_trade_client_extensions(authorization, account_id, trade_specifier, set_trade_client_extensions_body, accept_datetime_format=accept_datetime_format)

Set Trade Client Extensions

Update the Client Extensions for a Trade. Do not add, update, or delete the Client Extensions if your account is associated with MT4.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.set_trade_client_extensions200_response import SetTradeClientExtensions200Response
from pyfx.dispatch.oanda.models.set_trade_client_extensions_request import SetTradeClientExtensionsRequest
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    trade_specifier = 'trade_specifier_example' # str | Specifier for the Trade
    set_trade_client_extensions_body = pyfx.dispatch.oanda.SetTradeClientExtensionsRequest() # SetTradeClientExtensionsRequest | Details of how to modify the Trade's Client Extensions.
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)

    try:
        # Set Trade Client Extensions
        api_response = await api_instance.set_trade_client_extensions(authorization, account_id, trade_specifier, set_trade_client_extensions_body, accept_datetime_format=accept_datetime_format)
        print("The response of DefaultApi->set_trade_client_extensions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->set_trade_client_extensions: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **trade_specifier** | **str**| Specifier for the Trade | 
 **set_trade_client_extensions_body** | [**SetTradeClientExtensionsRequest**](SetTradeClientExtensionsRequest.md)| Details of how to modify the Trade&#39;s Client Extensions. | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 

### Return type

[**SetTradeClientExtensions200Response**](SetTradeClientExtensions200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Trade&#39;s Client Extensions have been updated as requested. |  * RequestID - The unique identifier generated for the request <br>  |
**400** | The Trade&#39;s Client Extensions cannot be modified as requested. |  -  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | The Account or Trade specified does not exist. |  -  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_trade_dependent_orders**
> SetTradeDependentOrders200Response set_trade_dependent_orders(authorization, account_id, trade_specifier, set_trade_dependent_orders_body, accept_datetime_format=accept_datetime_format)

Set Dependent Orders

Create, replace and cancel a Trade's dependent Orders (Take Profit, Stop Loss and Trailing Stop Loss) through the Trade itself

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.set_trade_dependent_orders200_response import SetTradeDependentOrders200Response
from pyfx.dispatch.oanda.models.set_trade_dependent_orders_request import SetTradeDependentOrdersRequest
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    trade_specifier = 'trade_specifier_example' # str | Specifier for the Trade
    set_trade_dependent_orders_body = pyfx.dispatch.oanda.SetTradeDependentOrdersRequest() # SetTradeDependentOrdersRequest | Details of how to modify the Trade's dependent Orders.
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)

    try:
        # Set Dependent Orders
        api_response = await api_instance.set_trade_dependent_orders(authorization, account_id, trade_specifier, set_trade_dependent_orders_body, accept_datetime_format=accept_datetime_format)
        print("The response of DefaultApi->set_trade_dependent_orders:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->set_trade_dependent_orders: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **trade_specifier** | **str**| Specifier for the Trade | 
 **set_trade_dependent_orders_body** | [**SetTradeDependentOrdersRequest**](SetTradeDependentOrdersRequest.md)| Details of how to modify the Trade&#39;s dependent Orders. | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 

### Return type

[**SetTradeDependentOrders200Response**](SetTradeDependentOrders200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Trade&#39;s dependent Orders have been modified as requested. |  * RequestID - The unique identifier generated for the request <br>  |
**400** | The Trade&#39;s dependent Orders cannot be modified as requested. |  -  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stream_pricing**
> StreamPricing200Response stream_pricing(authorization, account_id, instruments, accept_datetime_format=accept_datetime_format, snapshot=snapshot)

Price Stream

Get a stream of Account Prices starting from when the request is made. This pricing stream does not include every single price created for the Account, but instead will provide at most 4 prices per second (every 250 milliseconds) for each instrument being requested. If more than one price is created for an instrument during the 250 millisecond window, only the price in effect at the end of the window is sent. This means that during periods of rapid price movement, subscribers to this stream will not be sent every price. Pricing windows for different connections to the price stream are not all aligned in the same way (i.e. they are not all aligned to the top of the second). This means that during periods of rapid price movement, different subscribers may observe different prices depending on their alignment.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.stream_pricing200_response import StreamPricing200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier
    instruments = ['instruments_example'] # List[str] | List of Instruments to stream Prices for.
    accept_datetime_format = 'accept_datetime_format_example' # str | Format of DateTime fields in the request and response. (optional)
    snapshot = True # bool | Flag that enables/disables the sending of a pricing snapshot when initially connecting to the stream. (optional)

    try:
        # Price Stream
        api_response = await api_instance.stream_pricing(authorization, account_id, instruments, accept_datetime_format=accept_datetime_format, snapshot=snapshot)
        print("The response of DefaultApi->stream_pricing:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->stream_pricing: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 
 **instruments** | [**List[str]**](str.md)| List of Instruments to stream Prices for. | 
 **accept_datetime_format** | **str**| Format of DateTime fields in the request and response. | [optional] 
 **snapshot** | **bool**| Flag that enables/disables the sending of a pricing snapshot when initially connecting to the stream. | [optional] 

### Return type

[**StreamPricing200Response**](StreamPricing200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Connecting to the Price Stream was successful. |  * RequestID - The unique identifier generated for the request <br>  * Link - A link to the next page of results if the results were paginated <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stream_transactions**
> StreamTransactions200Response stream_transactions(authorization, account_id)

Transaction Stream

Get a stream of Transactions for an Account starting from when the request is made.

### Example

```python
import time
import os
import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.stream_transactions200_response import StreamTransactions200Response
from pyfx.dispatch.oanda.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /v3
# See configuration.py for a list of all supported configuration parameters.
configuration = pyfx.dispatch.oanda.Configuration(
    host = "/v3"
)


# Enter a context with an instance of the API client
async with pyfx.dispatch.oanda.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pyfx.dispatch.oanda.DefaultApi(api_client)
    authorization = 'authorization_example' # str | The authorization bearer token previously obtained by the client
    account_id = 'account_id_example' # str | Account Identifier

    try:
        # Transaction Stream
        api_response = await api_instance.stream_transactions(authorization, account_id)
        print("The response of DefaultApi->stream_transactions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->stream_transactions: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **str**| The authorization bearer token previously obtained by the client | 
 **account_id** | **str**| Account Identifier | 

### Return type

[**StreamTransactions200Response**](StreamTransactions200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Connecting to the Transaction Stream was successful. |  * RequestID - The unique identifier generated for the request <br>  |
**400** | Bad Request. The client has provided invalid data to be processed by the server. |  * RequestID - The unique identifier generated for the request <br>  |
**401** | Unauthorized. The endpoint being access required the client to authenticated, however the the authentication token is invalid or has not been provided. |  * RequestID - The unique identifier generated for the request <br>  |
**404** | Not Found. The client has attempted to access an entity that does not exist. |  * RequestID - The unique identifier generated for the request <br>  |
**405** | Method Not Allowed. The client has attempted to access an endpoint using an HTTP method that is not supported. |  * RequestID - The unique identifier generated for the request <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

