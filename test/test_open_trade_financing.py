
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.open_trade_financing import OpenTradeFinancing


class TestOpenTradeFinancing(ModelTest):
    """OpenTradeFinancing unit test stubs"""

    class Factory(MockFactory[OpenTradeFinancing]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
