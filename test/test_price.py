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
from pyfx.dispatch.oanda.models.price import Price  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestPrice(unittest.TestCase):
    """Price unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Price
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Price`
        """
        model = pyfx.dispatch.oanda.models.price.Price()  # noqa: E501
        if include_optional :
            return Price(
                instrument = '', 
                tradeable = True, 
                timestamp = '', 
                base_bid = '', 
                base_ask = '', 
                bids = [
                    pyfx.dispatch.oanda.models.price_bucket.PriceBucket(
                        price = '', 
                        liquidity = 56, )
                    ], 
                asks = [
                    pyfx.dispatch.oanda.models.price_bucket.PriceBucket(
                        price = '', 
                        liquidity = 56, )
                    ], 
                closeout_bid = '', 
                closeout_ask = ''
            )
        else :
            return Price(
        )
        """

    def testPrice(self):
        """Test Price"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
