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
from pyfx.dispatch.oanda.models.instruments_instrument_position_book_get200_response import InstrumentsInstrumentPositionBookGet200Response  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestInstrumentsInstrumentPositionBookGet200Response(unittest.TestCase):
    """InstrumentsInstrumentPositionBookGet200Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InstrumentsInstrumentPositionBookGet200Response
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `InstrumentsInstrumentPositionBookGet200Response`
        """
        model = pyfx.dispatch.oanda.models.instruments_instrument_position_book_get200_response.InstrumentsInstrumentPositionBookGet200Response()  # noqa: E501
        if include_optional :
            return InstrumentsInstrumentPositionBookGet200Response(
                position_book = pyfx.dispatch.oanda.models.position_book.PositionBook(
                    instrument = '', 
                    time = '', 
                    price = '', 
                    bucket_width = '', 
                    buckets = [
                        pyfx.dispatch.oanda.models.position_book_bucket.PositionBookBucket(
                            price = '', 
                            long_count_percent = '', 
                            short_count_percent = '', )
                        ], )
            )
        else :
            return InstrumentsInstrumentPositionBookGet200Response(
        )
        """

    def testInstrumentsInstrumentPositionBookGet200Response(self):
        """Test InstrumentsInstrumentPositionBookGet200Response"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
