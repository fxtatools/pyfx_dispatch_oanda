
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.set_trade_client_extensions404_response import SetTradeClientExtensions404Response


class TestSetTradeClientExtensions404Response(ModelTest):
    """SetTradeClientExtensions404Response unit test stubs"""

    class Factory(MockFactory[SetTradeClientExtensions404Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
