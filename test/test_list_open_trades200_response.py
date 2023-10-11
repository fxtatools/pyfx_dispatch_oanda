
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.list_open_trades200_response import ListOpenTrades200Response


class TestListOpenTrades200Response(ModelTest):
    """ListOpenTrades200Response unit test stubs"""

    class Factory(MockFactory[ListOpenTrades200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
