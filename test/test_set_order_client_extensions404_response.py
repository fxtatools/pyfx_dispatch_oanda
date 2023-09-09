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
from pyfx.dispatch.oanda.models.set_order_client_extensions404_response import SetOrderClientExtensions404Response  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestSetOrderClientExtensions404Response(unittest.TestCase):
    """SetOrderClientExtensions404Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SetOrderClientExtensions404Response
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SetOrderClientExtensions404Response`
        """
        model = pyfx.dispatch.oanda.models.set_order_client_extensions404_response.SetOrderClientExtensions404Response()  # noqa: E501
        if include_optional :
            return SetOrderClientExtensions404Response(
                order_client_extensions_modify_reject_transaction = pyfx.dispatch.oanda.models.order_client_extensions_modify_reject_transaction.OrderClientExtensionsModifyRejectTransaction(
                    id = '', 
                    time = '', 
                    user_id = 56, 
                    account_id = '', 
                    batch_id = '', 
                    request_id = '', 
                    type = 'CREATE', 
                    order_id = '', 
                    client_order_id = '', 
                    client_extensions_modify = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                        id = '', 
                        tag = '', 
                        comment = '', ), 
                    trade_client_extensions_modify = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                        id = '', 
                        tag = '', 
                        comment = '', ), 
                    reject_reason = 'INTERNAL_SERVER_ERROR', ), 
                last_transaction_id = '', 
                related_transaction_ids = [
                    ''
                    ], 
                error_code = '', 
                error_message = ''
            )
        else :
            return SetOrderClientExtensions404Response(
        )
        """

    def testSetOrderClientExtensions404Response(self):
        """Test SetOrderClientExtensions404Response"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
