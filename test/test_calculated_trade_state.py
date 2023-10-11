
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.calculated_trade_state import CalculatedTradeState


class TestCalculatedTradeState(ModelTest):
    """CalculatedTradeState unit test stubs"""

    class Factory(MockFactory[CalculatedTradeState]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
