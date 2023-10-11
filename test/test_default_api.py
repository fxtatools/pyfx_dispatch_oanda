## DefaultApi tests

import asyncio as aio
import unittest

from polyfactory.factories.attrs_factory import AttrsFactory

import pyfx.dispatch.oanda as subject

from pyfx.dispatch.oanda.test import run_tests

class TestDefaultApi(unittest.TestCase):
    """DefaultApi unit test stubs"""

    ## example = TestClientPrice.Factory
    ## obj = example.build()


    def setUp(self):
        self.loop = aio.get_event_loop_policy().get_event_loop()
        self.config = subject.Configuration(False, access_token="none")
        self.client = subject.ApiClient(self.loop, self.config)
        self.api = subject.DefaultApi(self.client)

    def tearDown(self):
        self.loop.run_until_complete(self.client.close)

    # def test_cancel_order(self):
    #     """Test case for cancel_order

    #     Cancel Order
    #     """
    #     pass

    # def test_close_trade(self):
    #     """Test case for close_trade

    #     Close Trade
    #     """
    #     pass

    # def test_configure_account(self):
    #     """Test case for configure_account

    #     Configure Account
    #     """
    #     pass

    # def test_create_order(self):
    #     """Test case for create_order

    #     Create Order
    #     """
    #     pass

    # def test_get_account(self):
    #     """Test case for get_account

    #     Account Details
    #     """
    #     pass

    # def test_get_account_changes(self):
    #     """Test case for get_account_changes

    #     Poll Account Updates
    #     """
    #     pass

    # def test_get_account_instruments(self):
    #     """Test case for get_account_instruments

    #     Account Instruments
    #     """
    #     pass

    # def test_get_account_summary(self):
    #     """Test case for get_account_summary

    #     Account Summary
    #     """
    #     pass

    # def test_get_base_prices(self):
    #     """Test case for get_base_prices

    #     Get Base Prices
    #     """
    #     pass

    # def test_get_external_user_info(self):
    #     """Test case for get_external_user_info

    #     External User Info
    #     """
    #     pass

    # def test_get_instrument_candles(self):
    #     """Test case for get_instrument_candles

    #     Get Candlesticks
    #     """
    #     pass

    # def test_get_instrument_candles_0(self):
    #     """Test case for get_instrument_candles_0

    #     Get Candlesticks
    #     """
    #     pass

    # def test_get_instrument_price(self):
    #     """Test case for get_instrument_price

    #     Price
    #     """
    #     pass

    # def test_get_instrument_price_range(self):
    #     """Test case for get_instrument_price_range

    #     Get Prices
    #     """
    #     pass

    # def test_get_order(self):
    #     """Test case for get_order

    #     Get Order
    #     """
    #     pass

    # def test_get_position(self):
    #     """Test case for get_position

    #     Instrument Position
    #     """
    #     pass

    # def test_get_price_range(self):
    #     """Test case for get_price_range

    #     Get Price Range
    #     """
    #     pass

    # def test_get_prices(self):
    #     """Test case for get_prices

    #     Current Account Prices
    #     """
    #     pass

    # def test_get_trade(self):
    #     """Test case for get_trade

    #     Trade Details
    #     """
    #     pass

    # def test_get_transaction(self):
    #     """Test case for get_transaction

    #     Transaction Details
    #     """
    #     pass

    # def test_get_transaction_range(self):
    #     """Test case for get_transaction_range

    #     Transaction ID Range
    #     """
    #     pass

    # def test_get_transactions_since_id(self):
    #     """Test case for get_transactions_since_id

    #     Transactions Since ID
    #     """
    #     pass

    # def test_get_user_info(self):
    #     """Test case for get_user_info

    #     User Info
    #     """
    #     pass

    # def test_instruments_instrument_order_book_get(self):
    #     """Test case for instruments_instrument_order_book_get

    #     Get Order Book
    #     """
    #     pass

    # def test_instruments_instrument_position_book_get(self):
    #     """Test case for instruments_instrument_position_book_get

    #     Get Position Book
    #     """
    #     pass

    # def test_list_accounts(self):
    #     """Test case for list_accounts

    #     List Accounts
    #     """
    #     pass

    # def test_list_open_positions(self):
    #     """Test case for list_open_positions

    #     Open Positions
    #     """
    #     pass

    # def test_list_open_trades(self):
    #     """Test case for list_open_trades

    #     List Open Trades
    #     """
    #     pass

    # def test_list_orders(self):
    #     """Test case for list_orders

    #     List Orders
    #     """
    #     pass

    # def test_list_pending_orders(self):
    #     """Test case for list_pending_orders

    #     Pending Orders
    #     """
    #     pass

    # def test_list_positions(self):
    #     """Test case for list_positions

    #     List Positions
    #     """
    #     pass

    # def test_list_trades(self):
    #     """Test case for list_trades

    #     List Trades
    #     """
    #     pass

    # def test_list_transactions(self):
    #     """Test case for list_transactions

    #     List Transactions
    #     """
    #     pass

    # def test_replace_order(self):
    #     """Test case for replace_order

    #     Replace Order
    #     """
    #     pass

    # def test_set_order_client_extensions(self):
    #     """Test case for set_order_client_extensions

    #     Set Order Extensions
    #     """
    #     pass

    # def test_set_trade_client_extensions(self):
    #     """Test case for set_trade_client_extensions

    #     Set Trade Client Extensions
    #     """
    #     pass

    # def test_set_trade_dependent_orders(self):
    #     """Test case for set_trade_dependent_orders

    #     Set Dependent Orders
    #     """
    #     pass

    # def test_stream_pricing(self):
    #     """Test case for stream_pricing

    #     Price Stream
    #     """
    #     pass

    # def test_stream_transactions(self):
    #     """Test case for stream_transactions

    #     Transaction Stream
    #     """
    #     pass


if __name__ == '__main__':
    run_tests(__file__)
