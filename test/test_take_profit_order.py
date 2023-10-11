
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.take_profit_order import TakeProfitOrder


class TestTakeProfitOrder(ModelTest):
    """TakeProfitOrder unit test stubs"""

    class Factory(MockFactory[TakeProfitOrder]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
