
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.quote_home_conversion_factors import QuoteHomeConversionFactors


class TestQuoteHomeConversionFactors(ModelTest):
    """QuoteHomeConversionFactors unit test stubs"""

    class Factory(MockFactory[QuoteHomeConversionFactors]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
