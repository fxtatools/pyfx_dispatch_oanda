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
from pyfx.dispatch.oanda.models.transfer_funds_reject_transaction import TransferFundsRejectTransaction  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestTransferFundsRejectTransaction(unittest.TestCase):
    """TransferFundsRejectTransaction unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TransferFundsRejectTransaction
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TransferFundsRejectTransaction`
        """
        model = pyfx.dispatch.oanda.models.transfer_funds_reject_transaction.TransferFundsRejectTransaction()  # noqa: E501
        if include_optional :
            return TransferFundsRejectTransaction(
                id = '', 
                time = '', 
                user_id = 56, 
                account_id = '', 
                batch_id = '', 
                request_id = '', 
                type = 'CREATE', 
                amount = '', 
                funding_reason = 'CLIENT_FUNDING', 
                comment = '', 
                reject_reason = 'INTERNAL_SERVER_ERROR'
            )
        else :
            return TransferFundsRejectTransaction(
        )
        """

    def testTransferFundsRejectTransaction(self):
        """Test TransferFundsRejectTransaction"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()