
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.delayed_trade_closure_transaction import DelayedTradeClosureTransaction


class TestDelayedTradeClosureTransaction(ModelTest):
    """DelayedTradeClosureTransaction unit test stubs"""

    class Factory(MockFactory[DelayedTradeClosureTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
