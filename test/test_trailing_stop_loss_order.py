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
from pyfx.dispatch.oanda.models.trailing_stop_loss_order import TrailingStopLossOrder  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestTrailingStopLossOrder(unittest.TestCase):
    """TrailingStopLossOrder unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TrailingStopLossOrder
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TrailingStopLossOrder`
        """
        model = pyfx.dispatch.oanda.models.trailing_stop_loss_order.TrailingStopLossOrder()  # noqa: E501
        if include_optional :
            return TrailingStopLossOrder(
                id = '', 
                create_time = '', 
                state = 'PENDING', 
                client_extensions = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                    id = '', 
                    tag = '', 
                    comment = '', ), 
                type = 'MARKET', 
                trade_id = '', 
                client_trade_id = '', 
                distance = '', 
                time_in_force = 'GTC', 
                gtd_time = '', 
                trigger_condition = 'DEFAULT', 
                trailing_stop_value = '', 
                filling_transaction_id = '', 
                filled_time = '', 
                trade_opened_id = '', 
                trade_reduced_id = '', 
                trade_closed_ids = [
                    ''
                    ], 
                cancelling_transaction_id = '', 
                cancelled_time = '', 
                replaces_order_id = '', 
                replaced_by_order_id = ''
            )
        else :
            return TrailingStopLossOrder(
        )
        """

    def testTrailingStopLossOrder(self):
        """Test TrailingStopLossOrder"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
