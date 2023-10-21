"""Unit test definition for pyfx.dispatch.oanda"""

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.set_trade_client_extensions400_response import SetTradeClientExtensions400Response


class TestSetTradeClientExtensions400Response(ModelTest):
    """SetTradeClientExtensions400Response unit test stubs"""

    class Factory(MockFactory[SetTradeClientExtensions400Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
