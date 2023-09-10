# pyfx.dispatch.oanda

## Overview

The pyfx.dispatch.oanda project provides a Python API supporting
asynchronous IO for HTTP operations with the OANDA v20 REST API.

The [OpenAPI specification for the OANDA v20 REST API](https://github.com/oanda/v20-openapi)
defines how to interact with v20 Accounts, Trades, Orders, Pricing and more.

## Origin

The pyfx.dispatch.oanda source code was automatically generated with an
application of the [OpenAPI Generator](https://openapi-generator.tech).

Build Information:

- OANDA v20 REST API version: 3.0.25
- pyfx.dispatch.oanda version: 1.0.0
- Generator: [python](https://openapi-generator.tech/docs/generators/python/)
- Build package: `org.openapitools.codegen.languages.PythonClientCodegen`

For more information about the OANDA v20 REST API, please visit
[the OANDA developer portal](http://developer.oanda.com/rest-live-v20/introduction/)

For more information about the OpenAPI Generator, please visit
[openapi-generator.tech](https://openapi-generator.tech/).

This project is not affiliated with OANDA, the OpenAPI Generator, or any
of their associated institutions.

## Requirements

Python 3.7+

## Installation & Usage

### pip install (Git)

The following shell commands can be used to create a Python virtual
environment, then installing the `pyfx.dispatch.oanda` source code
within the same environment.

The path to the environment's `activate` script may vary, by host
platform.

```sh
python -m venv env
source env/bin/activate
pip install git+https://github.com/fxtatools/pyfx_dispatch_oanda.git
```

### Setuptools

This project can be installed from source, using `pip`

```sh
python -m venv env
source env/bin/activate
pip install -e .
```

### Verifying the Installation

An example is available, below, for verifying the installation of the
API.

### Tests

Execute `pytest` to run the tests.

## Getting Started

After [installation](#installation--usage), the following example can be
used to print a summary of account codes for an account with an
authorized API token.

An API token is available
[via the Oanda hub](https://www.oanda.com/demo-account/tpa/personal_token).
Once created, the token should be stored securely.

For purpose of example, the token may be substituted in place of the
`<private_api_token>` text, below.

The `'Bearer '` prefix must be present, including the intermediate
space character (`' '`) in the complete authentication token.

This example will access the Oanda v20 server for demo trading accounts,
via HTTPS.

```python
import pyfx.dispatch.oanda as dispatch
import pyfx.dispatch.oanda.logging as dispatch_logging
from pprint import pprint

# Configure a debug-level console logger for the API
dispatch_logging.configure_debug_logger()

# Set host information and token for API requests
configuration = dispatch.Configuration(
    host = 'https://api-fxpractice.oanda.com/v3',
    access_token = '<private_api_token_>'
)

api_response = None

# Create an asynchronous context with an instance of the API client
async with dispatch.ApiClient(configuration) as api_client:
    ## Create an instance of the API class
    api_instance = dispatch.DefaultApi(api_client)
    ## Authentication bearer token for Oanda v20
    auth = 'Bearer %s' % configuration.access_token
    ## Send a single API request
    api_response = await api_instance.list_accounts(auth)

# print the result of the API query
if api_response:
    pprint(api_response.accounts)

```

A more expansive example is available in [examples/quotes.py](examples/quotes.py)

## Documentation for API Endpoints

The following documentation was created with OpenAPI Generator

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*DefaultApi* | [**cancel_order**](docs/DefaultApi.md#cancel_order) | **PUT** /accounts/{accountID}/orders/{orderSpecifier}/cancel | Cancel Order
*DefaultApi* | [**close_position**](docs/DefaultApi.md#close_position) | **PUT** /accounts/{accountID}/positions/{instrument}/close | Close Position
*DefaultApi* | [**close_trade**](docs/DefaultApi.md#close_trade) | **PUT** /accounts/{accountID}/trades/{tradeSpecifier}/close | Close Trade
*DefaultApi* | [**configure_account**](docs/DefaultApi.md#configure_account) | **PATCH** /accounts/{accountID}/configuration | Configure Account
*DefaultApi* | [**create_order**](docs/DefaultApi.md#create_order) | **POST** /accounts/{accountID}/orders | Create Order
*DefaultApi* | [**get_account**](docs/DefaultApi.md#get_account) | **GET** /accounts/{accountID} | Account Details
*DefaultApi* | [**get_account_changes**](docs/DefaultApi.md#get_account_changes) | **GET** /accounts/{accountID}/changes | Poll Account Updates
*DefaultApi* | [**get_account_instruments**](docs/DefaultApi.md#get_account_instruments) | **GET** /accounts/{accountID}/instruments | Account Instruments
*DefaultApi* | [**get_account_summary**](docs/DefaultApi.md#get_account_summary) | **GET** /accounts/{accountID}/summary | Account Summary
*DefaultApi* | [**get_base_prices**](docs/DefaultApi.md#get_base_prices) | **GET** /pricing | Get Base Prices
*DefaultApi* | [**get_external_user_info**](docs/DefaultApi.md#get_external_user_info) | **GET** /users/{userSpecifier}/externalInfo | External User Info
*DefaultApi* | [**get_instrument_candles**](docs/DefaultApi.md#get_instrument_candles) | **GET** /instruments/{instrument}/candles | Get Candlesticks
*DefaultApi* | [**get_instrument_candles_0**](docs/DefaultApi.md#get_instrument_candles_0) | **GET** /accounts/{accountID}/instruments/{instrument}/candles | Get Candlesticks
*DefaultApi* | [**get_instrument_price**](docs/DefaultApi.md#get_instrument_price) | **GET** /instruments/{instrument}/price | Price
*DefaultApi* | [**get_instrument_price_range**](docs/DefaultApi.md#get_instrument_price_range) | **GET** /instruments/{instrument}/price/range | Get Prices
*DefaultApi* | [**get_order**](docs/DefaultApi.md#get_order) | **GET** /accounts/{accountID}/orders/{orderSpecifier} | Get Order
*DefaultApi* | [**get_position**](docs/DefaultApi.md#get_position) | **GET** /accounts/{accountID}/positions/{instrument} | Instrument Position
*DefaultApi* | [**get_price_range**](docs/DefaultApi.md#get_price_range) | **GET** /pricing/range | Get Price Range
*DefaultApi* | [**get_prices**](docs/DefaultApi.md#get_prices) | **GET** /accounts/{accountID}/pricing | Current Account Prices
*DefaultApi* | [**get_trade**](docs/DefaultApi.md#get_trade) | **GET** /accounts/{accountID}/trades/{tradeSpecifier} | Trade Details
*DefaultApi* | [**get_transaction**](docs/DefaultApi.md#get_transaction) | **GET** /accounts/{accountID}/transactions/{transactionID} | Transaction Details
*DefaultApi* | [**get_transaction_range**](docs/DefaultApi.md#get_transaction_range) | **GET** /accounts/{accountID}/transactions/idrange | Transaction ID Range
*DefaultApi* | [**get_transactions_since_id**](docs/DefaultApi.md#get_transactions_since_id) | **GET** /accounts/{accountID}/transactions/sinceid | Transactions Since ID
*DefaultApi* | [**get_user_info**](docs/DefaultApi.md#get_user_info) | **GET** /users/{userSpecifier} | User Info
*DefaultApi* | [**instruments_instrument_order_book_get**](docs/DefaultApi.md#instruments_instrument_order_book_get) | **GET** /instruments/{instrument}/orderBook | Get Order Book
*DefaultApi* | [**instruments_instrument_position_book_get**](docs/DefaultApi.md#instruments_instrument_position_book_get) | **GET** /instruments/{instrument}/positionBook | Get Position Book
*DefaultApi* | [**list_accounts**](docs/DefaultApi.md#list_accounts) | **GET** /accounts | List Accounts
*DefaultApi* | [**list_open_positions**](docs/DefaultApi.md#list_open_positions) | **GET** /accounts/{accountID}/openPositions | Open Positions
*DefaultApi* | [**list_open_trades**](docs/DefaultApi.md#list_open_trades) | **GET** /accounts/{accountID}/openTrades | List Open Trades
*DefaultApi* | [**list_orders**](docs/DefaultApi.md#list_orders) | **GET** /accounts/{accountID}/orders | List Orders
*DefaultApi* | [**list_pending_orders**](docs/DefaultApi.md#list_pending_orders) | **GET** /accounts/{accountID}/pendingOrders | Pending Orders
*DefaultApi* | [**list_positions**](docs/DefaultApi.md#list_positions) | **GET** /accounts/{accountID}/positions | List Positions
*DefaultApi* | [**list_trades**](docs/DefaultApi.md#list_trades) | **GET** /accounts/{accountID}/trades | List Trades
*DefaultApi* | [**list_transactions**](docs/DefaultApi.md#list_transactions) | **GET** /accounts/{accountID}/transactions | List Transactions
*DefaultApi* | [**replace_order**](docs/DefaultApi.md#replace_order) | **PUT** /accounts/{accountID}/orders/{orderSpecifier} | Replace Order
*DefaultApi* | [**set_order_client_extensions**](docs/DefaultApi.md#set_order_client_extensions) | **PUT** /accounts/{accountID}/orders/{orderSpecifier}/clientExtensions | Set Order Extensions
*DefaultApi* | [**set_trade_client_extensions**](docs/DefaultApi.md#set_trade_client_extensions) | **PUT** /accounts/{accountID}/trades/{tradeSpecifier}/clientExtensions | Set Trade Client Extensions
*DefaultApi* | [**set_trade_dependent_orders**](docs/DefaultApi.md#set_trade_dependent_orders) | **PUT** /accounts/{accountID}/trades/{tradeSpecifier}/orders | Set Dependent Orders
*DefaultApi* | [**stream_pricing**](docs/DefaultApi.md#stream_pricing) | **GET** /accounts/{accountID}/pricing/stream | Price Stream
*DefaultApi* | [**stream_transactions**](docs/DefaultApi.md#stream_transactions) | **GET** /accounts/{accountID}/transactions/stream | Transaction Stream


## Documentation For Models

 - [AcceptDatetimeFormat](docs/AcceptDatetimeFormat.md)
 - [Account](docs/Account.md)
 - [AccountChanges](docs/AccountChanges.md)
 - [AccountChangesState](docs/AccountChangesState.md)
 - [AccountFinancingMode](docs/AccountFinancingMode.md)
 - [AccountProperties](docs/AccountProperties.md)
 - [AccountSummary](docs/AccountSummary.md)
 - [CalculatedAccountState](docs/CalculatedAccountState.md)
 - [CalculatedPositionState](docs/CalculatedPositionState.md)
 - [CalculatedTradeState](docs/CalculatedTradeState.md)
 - [CancelOrder200Response](docs/CancelOrder200Response.md)
 - [CancelOrder404Response](docs/CancelOrder404Response.md)
 - [CancellableOrderType](docs/CancellableOrderType.md)
 - [Candlestick](docs/Candlestick.md)
 - [CandlestickData](docs/CandlestickData.md)
 - [CandlestickGranularity](docs/CandlestickGranularity.md)
 - [ClientConfigureRejectTransaction](docs/ClientConfigureRejectTransaction.md)
 - [ClientConfigureTransaction](docs/ClientConfigureTransaction.md)
 - [ClientExtensions](docs/ClientExtensions.md)
 - [ClientPrice](docs/ClientPrice.md)
 - [ClosePosition200Response](docs/ClosePosition200Response.md)
 - [ClosePosition400Response](docs/ClosePosition400Response.md)
 - [ClosePosition404Response](docs/ClosePosition404Response.md)
 - [ClosePositionRequest](docs/ClosePositionRequest.md)
 - [CloseTrade200Response](docs/CloseTrade200Response.md)
 - [CloseTrade400Response](docs/CloseTrade400Response.md)
 - [CloseTrade404Response](docs/CloseTrade404Response.md)
 - [CloseTradeRequest](docs/CloseTradeRequest.md)
 - [CloseTransaction](docs/CloseTransaction.md)
 - [ConfigureAccount200Response](docs/ConfigureAccount200Response.md)
 - [ConfigureAccount400Response](docs/ConfigureAccount400Response.md)
 - [ConfigureAccountRequest](docs/ConfigureAccountRequest.md)
 - [CreateOrder201Response](docs/CreateOrder201Response.md)
 - [CreateOrder400Response](docs/CreateOrder400Response.md)
 - [CreateOrder404Response](docs/CreateOrder404Response.md)
 - [CreateOrderRequest](docs/CreateOrderRequest.md)
 - [CreateTransaction](docs/CreateTransaction.md)
 - [DailyFinancingTransaction](docs/DailyFinancingTransaction.md)
 - [DelayedTradeClosureTransaction](docs/DelayedTradeClosureTransaction.md)
 - [Direction](docs/Direction.md)
 - [DynamicOrderState](docs/DynamicOrderState.md)
 - [FixedPriceOrder](docs/FixedPriceOrder.md)
 - [FixedPriceOrderReason](docs/FixedPriceOrderReason.md)
 - [FixedPriceOrderTransaction](docs/FixedPriceOrderTransaction.md)
 - [FundingReason](docs/FundingReason.md)
 - [GetAccount200Response](docs/GetAccount200Response.md)
 - [GetAccountChanges200Response](docs/GetAccountChanges200Response.md)
 - [GetAccountInstruments200Response](docs/GetAccountInstruments200Response.md)
 - [GetAccountSummary200Response](docs/GetAccountSummary200Response.md)
 - [GetExternalUserInfo200Response](docs/GetExternalUserInfo200Response.md)
 - [GetInstrumentCandles200Response](docs/GetInstrumentCandles200Response.md)
 - [GetInstrumentCandles400Response](docs/GetInstrumentCandles400Response.md)
 - [GetInstrumentPrice200Response](docs/GetInstrumentPrice200Response.md)
 - [GetInstrumentPriceRange200Response](docs/GetInstrumentPriceRange200Response.md)
 - [GetOrder200Response](docs/GetOrder200Response.md)
 - [GetPosition200Response](docs/GetPosition200Response.md)
 - [GetPrices200Response](docs/GetPrices200Response.md)
 - [GetTrade200Response](docs/GetTrade200Response.md)
 - [GetTransaction200Response](docs/GetTransaction200Response.md)
 - [GetTransactionRange200Response](docs/GetTransactionRange200Response.md)
 - [GetUserInfo200Response](docs/GetUserInfo200Response.md)
 - [GuaranteedStopLossOrderEntryData](docs/GuaranteedStopLossOrderEntryData.md)
 - [GuaranteedStopLossOrderLevelRestriction](docs/GuaranteedStopLossOrderLevelRestriction.md)
 - [GuaranteedStopLossOrderMode](docs/GuaranteedStopLossOrderMode.md)
 - [HomeConversions](docs/HomeConversions.md)
 - [Instrument](docs/Instrument.md)
 - [InstrumentCommission](docs/InstrumentCommission.md)
 - [InstrumentType](docs/InstrumentType.md)
 - [InstrumentsInstrumentOrderBookGet200Response](docs/InstrumentsInstrumentOrderBookGet200Response.md)
 - [InstrumentsInstrumentPositionBookGet200Response](docs/InstrumentsInstrumentPositionBookGet200Response.md)
 - [LimitOrder](docs/LimitOrder.md)
 - [LimitOrderReason](docs/LimitOrderReason.md)
 - [LimitOrderRejectTransaction](docs/LimitOrderRejectTransaction.md)
 - [LimitOrderRequest](docs/LimitOrderRequest.md)
 - [LimitOrderTransaction](docs/LimitOrderTransaction.md)
 - [LiquidityRegenerationSchedule](docs/LiquidityRegenerationSchedule.md)
 - [LiquidityRegenerationScheduleStep](docs/LiquidityRegenerationScheduleStep.md)
 - [ListAccounts200Response](docs/ListAccounts200Response.md)
 - [ListOpenPositions200Response](docs/ListOpenPositions200Response.md)
 - [ListOpenTrades200Response](docs/ListOpenTrades200Response.md)
 - [ListOrders200Response](docs/ListOrders200Response.md)
 - [ListPendingOrders200Response](docs/ListPendingOrders200Response.md)
 - [ListPositions200Response](docs/ListPositions200Response.md)
 - [ListTrades200Response](docs/ListTrades200Response.md)
 - [ListTransactions200Response](docs/ListTransactions200Response.md)
 - [MT4TransactionHeartbeat](docs/MT4TransactionHeartbeat.md)
 - [MarginCallEnterTransaction](docs/MarginCallEnterTransaction.md)
 - [MarginCallExitTransaction](docs/MarginCallExitTransaction.md)
 - [MarginCallExtendTransaction](docs/MarginCallExtendTransaction.md)
 - [MarketIfTouchedOrder](docs/MarketIfTouchedOrder.md)
 - [MarketIfTouchedOrderReason](docs/MarketIfTouchedOrderReason.md)
 - [MarketIfTouchedOrderRejectTransaction](docs/MarketIfTouchedOrderRejectTransaction.md)
 - [MarketIfTouchedOrderRequest](docs/MarketIfTouchedOrderRequest.md)
 - [MarketIfTouchedOrderTransaction](docs/MarketIfTouchedOrderTransaction.md)
 - [MarketOrder](docs/MarketOrder.md)
 - [MarketOrderDelayedTradeClose](docs/MarketOrderDelayedTradeClose.md)
 - [MarketOrderMarginCloseout](docs/MarketOrderMarginCloseout.md)
 - [MarketOrderMarginCloseoutReason](docs/MarketOrderMarginCloseoutReason.md)
 - [MarketOrderPositionCloseout](docs/MarketOrderPositionCloseout.md)
 - [MarketOrderReason](docs/MarketOrderReason.md)
 - [MarketOrderRejectTransaction](docs/MarketOrderRejectTransaction.md)
 - [MarketOrderRequest](docs/MarketOrderRequest.md)
 - [MarketOrderTradeClose](docs/MarketOrderTradeClose.md)
 - [MarketOrderTransaction](docs/MarketOrderTransaction.md)
 - [OpenTradeFinancing](docs/OpenTradeFinancing.md)
 - [Order](docs/Order.md)
 - [OrderBook](docs/OrderBook.md)
 - [OrderBookBucket](docs/OrderBookBucket.md)
 - [OrderCancelReason](docs/OrderCancelReason.md)
 - [OrderCancelRejectTransaction](docs/OrderCancelRejectTransaction.md)
 - [OrderCancelTransaction](docs/OrderCancelTransaction.md)
 - [OrderClientExtensionsModifyRejectTransaction](docs/OrderClientExtensionsModifyRejectTransaction.md)
 - [OrderClientExtensionsModifyTransaction](docs/OrderClientExtensionsModifyTransaction.md)
 - [OrderFillReason](docs/OrderFillReason.md)
 - [OrderFillTransaction](docs/OrderFillTransaction.md)
 - [OrderIdentifier](docs/OrderIdentifier.md)
 - [OrderPositionFill](docs/OrderPositionFill.md)
 - [OrderState](docs/OrderState.md)
 - [OrderStateFilter](docs/OrderStateFilter.md)
 - [OrderTriggerCondition](docs/OrderTriggerCondition.md)
 - [OrderType](docs/OrderType.md)
 - [Position](docs/Position.md)
 - [PositionAggregationMode](docs/PositionAggregationMode.md)
 - [PositionBook](docs/PositionBook.md)
 - [PositionBookBucket](docs/PositionBookBucket.md)
 - [PositionFinancing](docs/PositionFinancing.md)
 - [PositionSide](docs/PositionSide.md)
 - [Price](docs/Price.md)
 - [PriceBucket](docs/PriceBucket.md)
 - [PriceStatus](docs/PriceStatus.md)
 - [PricingHeartbeat](docs/PricingHeartbeat.md)
 - [QuoteHomeConversionFactors](docs/QuoteHomeConversionFactors.md)
 - [ReopenTransaction](docs/ReopenTransaction.md)
 - [ReplaceOrder201Response](docs/ReplaceOrder201Response.md)
 - [ReplaceOrder400Response](docs/ReplaceOrder400Response.md)
 - [ReplaceOrder404Response](docs/ReplaceOrder404Response.md)
 - [ResetResettablePLTransaction](docs/ResetResettablePLTransaction.md)
 - [SetOrderClientExtensions200Response](docs/SetOrderClientExtensions200Response.md)
 - [SetOrderClientExtensions400Response](docs/SetOrderClientExtensions400Response.md)
 - [SetOrderClientExtensions404Response](docs/SetOrderClientExtensions404Response.md)
 - [SetOrderClientExtensionsRequest](docs/SetOrderClientExtensionsRequest.md)
 - [SetTradeClientExtensions200Response](docs/SetTradeClientExtensions200Response.md)
 - [SetTradeClientExtensions400Response](docs/SetTradeClientExtensions400Response.md)
 - [SetTradeClientExtensions404Response](docs/SetTradeClientExtensions404Response.md)
 - [SetTradeClientExtensionsRequest](docs/SetTradeClientExtensionsRequest.md)
 - [SetTradeDependentOrders200Response](docs/SetTradeDependentOrders200Response.md)
 - [SetTradeDependentOrders400Response](docs/SetTradeDependentOrders400Response.md)
 - [SetTradeDependentOrdersRequest](docs/SetTradeDependentOrdersRequest.md)
 - [StopLossDetails](docs/StopLossDetails.md)
 - [StopLossOrder](docs/StopLossOrder.md)
 - [StopLossOrderReason](docs/StopLossOrderReason.md)
 - [StopLossOrderRejectTransaction](docs/StopLossOrderRejectTransaction.md)
 - [StopLossOrderRequest](docs/StopLossOrderRequest.md)
 - [StopLossOrderTransaction](docs/StopLossOrderTransaction.md)
 - [StopOrder](docs/StopOrder.md)
 - [StopOrderReason](docs/StopOrderReason.md)
 - [StopOrderRejectTransaction](docs/StopOrderRejectTransaction.md)
 - [StopOrderRequest](docs/StopOrderRequest.md)
 - [StopOrderTransaction](docs/StopOrderTransaction.md)
 - [StreamPricing200Response](docs/StreamPricing200Response.md)
 - [StreamTransactions200Response](docs/StreamTransactions200Response.md)
 - [TakeProfitDetails](docs/TakeProfitDetails.md)
 - [TakeProfitOrder](docs/TakeProfitOrder.md)
 - [TakeProfitOrderReason](docs/TakeProfitOrderReason.md)
 - [TakeProfitOrderRejectTransaction](docs/TakeProfitOrderRejectTransaction.md)
 - [TakeProfitOrderRequest](docs/TakeProfitOrderRequest.md)
 - [TakeProfitOrderTransaction](docs/TakeProfitOrderTransaction.md)
 - [TimeInForce](docs/TimeInForce.md)
 - [Trade](docs/Trade.md)
 - [TradeClientExtensionsModifyRejectTransaction](docs/TradeClientExtensionsModifyRejectTransaction.md)
 - [TradeClientExtensionsModifyTransaction](docs/TradeClientExtensionsModifyTransaction.md)
 - [TradeOpen](docs/TradeOpen.md)
 - [TradePL](docs/TradePL.md)
 - [TradeReduce](docs/TradeReduce.md)
 - [TradeState](docs/TradeState.md)
 - [TradeStateFilter](docs/TradeStateFilter.md)
 - [TradeSummary](docs/TradeSummary.md)
 - [TrailingStopLossDetails](docs/TrailingStopLossDetails.md)
 - [TrailingStopLossOrder](docs/TrailingStopLossOrder.md)
 - [TrailingStopLossOrderReason](docs/TrailingStopLossOrderReason.md)
 - [TrailingStopLossOrderRejectTransaction](docs/TrailingStopLossOrderRejectTransaction.md)
 - [TrailingStopLossOrderRequest](docs/TrailingStopLossOrderRequest.md)
 - [TrailingStopLossOrderTransaction](docs/TrailingStopLossOrderTransaction.md)
 - [Transaction](docs/Transaction.md)
 - [TransactionFilter](docs/TransactionFilter.md)
 - [TransactionHeartbeat](docs/TransactionHeartbeat.md)
 - [TransactionRejectReason](docs/TransactionRejectReason.md)
 - [TransactionType](docs/TransactionType.md)
 - [TransferFundsRejectTransaction](docs/TransferFundsRejectTransaction.md)
 - [TransferFundsTransaction](docs/TransferFundsTransaction.md)
 - [UnitsAvailable](docs/UnitsAvailable.md)
 - [UnitsAvailableDetails](docs/UnitsAvailableDetails.md)
 - [UserInfo](docs/UserInfo.md)
 - [UserInfoExternal](docs/UserInfoExternal.md)
 - [WeeklyAlignment](docs/WeeklyAlignment.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization

See example, above

## Author

The [OANDA v20 OpenAPI spec](https://github.com/oanda/v20-openapi) is
published by OANDA at GitHub.

The version used in creating this project:
[3.0.25](https://github.com/oanda/v20-openapi/releases/tag/3.0.25)

This project is not affiliated with OANDA, the OpenAPI Generator, or any
of their associated institutions.
