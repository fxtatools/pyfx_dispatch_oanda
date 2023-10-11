
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.set_trade_client_extensions_request import SetTradeClientExtensionsRequest


class TestSetTradeClientExtensionsRequest(ModelTest):
    """SetTradeClientExtensionsRequest unit test stubs"""

    class Factory(MockFactory[SetTradeClientExtensionsRequest]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
