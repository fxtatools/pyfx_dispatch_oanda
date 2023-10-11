
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.take_profit_order_request import TakeProfitOrderRequest


class TestTakeProfitOrderRequest(ModelTest):
    """TakeProfitOrderRequest unit test stubs"""

    class Factory(MockFactory[TakeProfitOrderRequest]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
