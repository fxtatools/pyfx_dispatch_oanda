
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.close_trade_request import CloseTradeRequest


class TestCloseTradeRequest(ModelTest):
    """CloseTradeRequest unit test stubs"""

    class Factory(MockFactory[CloseTradeRequest]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
