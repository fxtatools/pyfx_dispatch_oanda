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
from pyfx.dispatch.oanda.models.position_side import PositionSide  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestPositionSide(unittest.TestCase):
    """PositionSide unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PositionSide
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PositionSide`
        """
        model = pyfx.dispatch.oanda.models.position_side.PositionSide()  # noqa: E501
        if include_optional :
            return PositionSide(
                units = '', 
                average_price = '', 
                trade_ids = [
                    ''
                    ], 
                pl = '', 
                unrealized_pl = '', 
                resettable_pl = '', 
                financing = '', 
                guaranteed_execution_fees = ''
            )
        else :
            return PositionSide(
        )
        """

    def testPositionSide(self):
        """Test PositionSide"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
