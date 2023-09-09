# coding: utf-8

"""
    OANDA v20 REST API

    The full OANDA v20 REST API Specification. This specification defines how to interact with v20 Accounts, Trades, Orders, Pricing and more.

    The version of the OpenAPI document: 3.0.25
    Contact: api@oanda.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.market_order_reject_transaction import MarketOrderRejectTransaction  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestMarketOrderRejectTransaction(unittest.TestCase):
    """MarketOrderRejectTransaction unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test MarketOrderRejectTransaction
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `MarketOrderRejectTransaction`
        """
        model = pyfx.dispatch.oanda.models.market_order_reject_transaction.MarketOrderRejectTransaction()  # noqa: E501
        if include_optional :
            return MarketOrderRejectTransaction(
                id = '', 
                time = '', 
                user_id = 56, 
                account_id = '', 
                batch_id = '', 
                request_id = '', 
                type = 'CREATE', 
                instrument = '', 
                units = '', 
                time_in_force = 'GTC', 
                price_bound = '', 
                position_fill = 'OPEN_ONLY', 
                trade_close = pyfx.dispatch.oanda.models.market_order_trade_close.MarketOrderTradeClose(
                    trade_id = '', 
                    client_trade_id = '', 
                    units = '', ), 
                long_position_closeout = pyfx.dispatch.oanda.models.market_order_position_closeout.MarketOrderPositionCloseout(
                    instrument = '', 
                    units = '', ), 
                short_position_closeout = pyfx.dispatch.oanda.models.market_order_position_closeout.MarketOrderPositionCloseout(
                    instrument = '', 
                    units = '', ), 
                margin_closeout = pyfx.dispatch.oanda.models.market_order_margin_closeout.MarketOrderMarginCloseout(
                    reason = 'MARGIN_CHECK_VIOLATION', ), 
                delayed_trade_close = pyfx.dispatch.oanda.models.market_order_delayed_trade_close.MarketOrderDelayedTradeClose(
                    trade_id = '', 
                    client_trade_id = '', 
                    source_transaction_id = '', ), 
                reason = 'CLIENT_ORDER', 
                client_extensions = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                    id = '', 
                    tag = '', 
                    comment = '', ), 
                take_profit_on_fill = pyfx.dispatch.oanda.models.take_profit_details.TakeProfitDetails(
                    price = '', 
                    time_in_force = 'GTC', 
                    gtd_time = '', 
                    client_extensions = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                        id = '', 
                        tag = '', 
                        comment = '', ), ), 
                stop_loss_on_fill = pyfx.dispatch.oanda.models.stop_loss_details.StopLossDetails(
                    price = '', 
                    distance = '', 
                    time_in_force = 'GTC', 
                    gtd_time = '', 
                    client_extensions = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                        id = '', 
                        tag = '', 
                        comment = '', ), 
                    guaranteed = True, ), 
                trailing_stop_loss_on_fill = pyfx.dispatch.oanda.models.trailing_stop_loss_details.TrailingStopLossDetails(
                    distance = '', 
                    time_in_force = 'GTC', 
                    gtd_time = '', 
                    client_extensions = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                        id = '', 
                        tag = '', 
                        comment = '', ), ), 
                trade_client_extensions = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                    id = '', 
                    tag = '', 
                    comment = '', ), 
                reject_reason = 'INTERNAL_SERVER_ERROR'
            )
        else :
            return MarketOrderRejectTransaction(
        )
        """

    def testMarketOrderRejectTransaction(self):
        """Test MarketOrderRejectTransaction"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
