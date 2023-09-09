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
from pyfx.dispatch.oanda.models.limit_order_transaction import LimitOrderTransaction  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestLimitOrderTransaction(unittest.TestCase):
    """LimitOrderTransaction unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test LimitOrderTransaction
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `LimitOrderTransaction`
        """
        model = pyfx.dispatch.oanda.models.limit_order_transaction.LimitOrderTransaction()  # noqa: E501
        if include_optional :
            return LimitOrderTransaction(
                id = '', 
                time = '', 
                user_id = 56, 
                account_id = '', 
                batch_id = '', 
                request_id = '', 
                type = 'CREATE', 
                instrument = '', 
                units = '', 
                price = '', 
                time_in_force = 'GTC', 
                gtd_time = '', 
                position_fill = 'OPEN_ONLY', 
                trigger_condition = 'DEFAULT', 
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
                replaces_order_id = '', 
                cancelling_transaction_id = ''
            )
        else :
            return LimitOrderTransaction(
        )
        """

    def testLimitOrderTransaction(self):
        """Test LimitOrderTransaction"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
