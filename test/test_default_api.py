# coding: utf-8

import asyncio as aio
import unittest

import pyfx.dispatch.oanda as context


class TestDefaultApi(unittest.TestCase):
    """DefaultApi unit test stubs"""

    def setUp(self):
        loop = aio.get_event_loop_policy().get_event_loop()
        config = context.Configuration("https://beta.example.com")
        client = context.ApiClient(loop, config)
        self.api = context.DefaultApi(client)  # noqa: E501

    def tearDown(self):
        pass

    def test_cancel_order(self):
        """Test case for cancel_order

        Cancel Order  # noqa: E501
        """
        pass

    def test_close_position(self):
        """Test case for close_position

        Close Position  # noqa: E501
        """
        pass

    def test_close_trade(self):
        """Test case for close_trade

        Close Trade  # noqa: E501
        """
        pass

    def test_configure_account(self):
        """Test case for configure_account

        Configure Account  # noqa: E501
        """
        pass

    def test_create_order(self):
        """Test case for create_order

        Create Order  # noqa: E501
        """
        pass

    def test_get_account(self):
        """Test case for get_account

        Account Details  # noqa: E501
        """
        pass

    def test_get_account_changes(self):
        """Test case for get_account_changes

        Poll Account Updates  # noqa: E501
        """
        pass

    def test_get_account_instruments(self):
        """Test case for get_account_instruments

        Account Instruments  # noqa: E501
        """
        pass

    def test_get_account_summary(self):
        """Test case for get_account_summary

        Account Summary  # noqa: E501
        """
        pass

    def test_get_base_prices(self):
        """Test case for get_base_prices

        Get Base Prices  # noqa: E501
        """
        pass

    def test_get_external_user_info(self):
        """Test case for get_external_user_info

        External User Info  # noqa: E501
        """
        pass

    def test_get_instrument_candles(self):
        """Test case for get_instrument_candles

        Get Candlesticks  # noqa: E501
        """
        pass

    def test_get_instrument_candles_0(self):
        """Test case for get_instrument_candles_0

        Get Candlesticks  # noqa: E501
        """
        pass

    def test_get_instrument_price(self):
        """Test case for get_instrument_price

        Price  # noqa: E501
        """
        pass

    def test_get_instrument_price_range(self):
        """Test case for get_instrument_price_range

        Get Prices  # noqa: E501
        """
        pass

    def test_get_order(self):
        """Test case for get_order

        Get Order  # noqa: E501
        """
        pass

    def test_get_position(self):
        """Test case for get_position

        Instrument Position  # noqa: E501
        """
        pass

    def test_get_price_range(self):
        """Test case for get_price_range

        Get Price Range  # noqa: E501
        """
        pass

    def test_get_prices(self):
        """Test case for get_prices

        Current Account Prices  # noqa: E501
        """
        pass

    def test_get_trade(self):
        """Test case for get_trade

        Trade Details  # noqa: E501
        """
        pass

    def test_get_transaction(self):
        """Test case for get_transaction

        Transaction Details  # noqa: E501
        """
        pass

    def test_get_transaction_range(self):
        """Test case for get_transaction_range

        Transaction ID Range  # noqa: E501
        """
        pass

    def test_get_transactions_since_id(self):
        """Test case for get_transactions_since_id

        Transactions Since ID  # noqa: E501
        """
        pass

    def test_get_user_info(self):
        """Test case for get_user_info

        User Info  # noqa: E501
        """
        pass

    def test_instruments_instrument_order_book_get(self):
        """Test case for instruments_instrument_order_book_get

        Get Order Book  # noqa: E501
        """
        pass

    def test_instruments_instrument_position_book_get(self):
        """Test case for instruments_instrument_position_book_get

        Get Position Book  # noqa: E501
        """
        pass

    def test_list_accounts(self):
        """Test case for list_accounts

        List Accounts  # noqa: E501
        """
        pass

    def test_list_open_positions(self):
        """Test case for list_open_positions

        Open Positions  # noqa: E501
        """
        pass

    def test_list_open_trades(self):
        """Test case for list_open_trades

        List Open Trades  # noqa: E501
        """
        pass

    def test_list_orders(self):
        """Test case for list_orders

        List Orders  # noqa: E501
        """
        pass

    def test_list_pending_orders(self):
        """Test case for list_pending_orders

        Pending Orders  # noqa: E501
        """
        pass

    def test_list_positions(self):
        """Test case for list_positions

        List Positions  # noqa: E501
        """
        pass

    def test_list_trades(self):
        """Test case for list_trades

        List Trades  # noqa: E501
        """
        pass

    def test_list_transactions(self):
        """Test case for list_transactions

        List Transactions  # noqa: E501
        """
        pass

    def test_replace_order(self):
        """Test case for replace_order

        Replace Order  # noqa: E501
        """
        pass

    def test_set_order_client_extensions(self):
        """Test case for set_order_client_extensions

        Set Order Extensions  # noqa: E501
        """
        pass

    def test_set_trade_client_extensions(self):
        """Test case for set_trade_client_extensions

        Set Trade Client Extensions  # noqa: E501
        """
        pass

    def test_set_trade_dependent_orders(self):
        """Test case for set_trade_dependent_orders

        Set Dependent Orders  # noqa: E501
        """
        pass

    def test_stream_pricing(self):
        """Test case for stream_pricing

        Price Stream  # noqa: E501
        """
        pass

    def test_stream_transactions(self):
        """Test case for stream_transactions

        Transaction Stream  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
