# coding: utf-8

"""
    OANDA v20 REST API

    The full OANDA v20 REST API Specification. This specification defines how to interact with v20 Accounts, Trades, Orders, Pricing and more.

    The version of the OpenAPI document: 3.0.25

    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.take_profit_order_reject_transaction import TakeProfitOrderRejectTransaction  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestTakeProfitOrderRejectTransaction(unittest.TestCase):
    """TakeProfitOrderRejectTransaction unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TakeProfitOrderRejectTransaction
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TakeProfitOrderRejectTransaction`
        """
        model = pyfx.dispatch.oanda.models.take_profit_order_reject_transaction.TakeProfitOrderRejectTransaction()  # noqa: E501
        if include_optional :
            return TakeProfitOrderRejectTransaction(
                id = '', 
                time = '', 
                user_id = 56, 
                account_id = '', 
                batch_id = '', 
                request_id = '', 
                type = 'CREATE', 
                trade_id = '', 
                client_trade_id = '', 
                price = '', 
                time_in_force = 'GTC', 
                gtd_time = '', 
                trigger_condition = 'DEFAULT', 
                reason = 'CLIENT_ORDER', 
                client_extensions = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                    id = '', 
                    tag = '', 
                    comment = '', ), 
                order_fill_transaction_id = '', 
                intended_replaces_order_id = '', 
                reject_reason = 'INTERNAL_SERVER_ERROR'
            )
        else :
            return TakeProfitOrderRejectTransaction(
        )
        """

    def testTakeProfitOrderRejectTransaction(self):
        """Test TakeProfitOrderRejectTransaction"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
