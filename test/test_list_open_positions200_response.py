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
from pyfx.dispatch.oanda.models.list_open_positions200_response import ListOpenPositions200Response  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestListOpenPositions200Response(unittest.TestCase):
    """ListOpenPositions200Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ListOpenPositions200Response
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ListOpenPositions200Response`
        """
        model = pyfx.dispatch.oanda.models.list_open_positions200_response.ListOpenPositions200Response()  # noqa: E501
        if include_optional :
            return ListOpenPositions200Response(
                positions = [
                    pyfx.dispatch.oanda.models.position.Position(
                        instrument = '', 
                        pl = '', 
                        unrealized_pl = '', 
                        margin_used = '', 
                        resettable_pl = '', 
                        financing = '', 
                        commission = '', 
                        guaranteed_execution_fees = '', 
                        long = pyfx.dispatch.oanda.models.position_side.PositionSide(
                            units = '', 
                            average_price = '', 
                            trade_ids = [
                                ''
                                ], 
                            pl = '', 
                            unrealized_pl = '', 
                            resettable_pl = '', 
                            financing = '', 
                            guaranteed_execution_fees = '', ), 
                        short = pyfx.dispatch.oanda.models.position_side.PositionSide(
                            units = '', 
                            average_price = '', 
                            pl = '', 
                            unrealized_pl = '', 
                            resettable_pl = '', 
                            financing = '', 
                            guaranteed_execution_fees = '', ), )
                    ], 
                last_transaction_id = ''
            )
        else :
            return ListOpenPositions200Response(
        )
        """

    def testListOpenPositions200Response(self):
        """Test ListOpenPositions200Response"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
