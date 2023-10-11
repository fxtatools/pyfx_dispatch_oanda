
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.get_trade200_response import GetTrade200Response


class TestGetTrade200Response(ModelTest):
    """GetTrade200Response unit test stubs"""

    class Factory(MockFactory[GetTrade200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
