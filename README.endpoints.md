Documentation for API Endpoints
===============================

The following documentation was created with OpenAPI Generator

See also: [Documentation for Models](./README.models.md)

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
