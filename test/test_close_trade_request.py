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
from pyfx.dispatch.oanda.models.close_trade_request import CloseTradeRequest  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestCloseTradeRequest(unittest.TestCase):
    """CloseTradeRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CloseTradeRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CloseTradeRequest`
        """
        model = pyfx.dispatch.oanda.models.close_trade_request.CloseTradeRequest()  # noqa: E501
        if include_optional :
            return CloseTradeRequest(
                units = ''
            )
        else :
            return CloseTradeRequest(
        )
        """

    def testCloseTradeRequest(self):
        """Test CloseTradeRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()