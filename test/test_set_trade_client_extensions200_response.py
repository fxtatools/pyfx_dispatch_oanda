
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.set_trade_client_extensions200_response import SetTradeClientExtensions200Response


class TestSetTradeClientExtensions200Response(ModelTest):
    """SetTradeClientExtensions200Response unit test stubs"""

    class Factory(MockFactory[SetTradeClientExtensions200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
