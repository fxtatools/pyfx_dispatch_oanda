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
from pyfx.dispatch.oanda.models.trade_client_extensions_modify_transaction import TradeClientExtensionsModifyTransaction  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestTradeClientExtensionsModifyTransaction(unittest.TestCase):
    """TradeClientExtensionsModifyTransaction unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TradeClientExtensionsModifyTransaction
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TradeClientExtensionsModifyTransaction`
        """
        model = pyfx.dispatch.oanda.models.trade_client_extensions_modify_transaction.TradeClientExtensionsModifyTransaction()  # noqa: E501
        if include_optional :
            return TradeClientExtensionsModifyTransaction(
                id = '', 
                time = '', 
                user_id = 56, 
                account_id = '', 
                batch_id = '', 
                request_id = '', 
                type = 'CREATE', 
                trade_id = '', 
                client_trade_id = '', 
                trade_client_extensions_modify = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                    id = '', 
                    tag = '', 
                    comment = '', )
            )
        else :
            return TradeClientExtensionsModifyTransaction(
        )
        """

    def testTradeClientExtensionsModifyTransaction(self):
        """Test TradeClientExtensionsModifyTransaction"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
