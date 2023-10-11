
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.get_prices200_response import GetPrices200Response


class TestGetPrices200Response(ModelTest):
    """GetPrices200Response unit test stubs"""

    class Factory(MockFactory[GetPrices200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
