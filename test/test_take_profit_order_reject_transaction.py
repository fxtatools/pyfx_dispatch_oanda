
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.take_profit_order_reject_transaction import TakeProfitOrderRejectTransaction


class TestTakeProfitOrderRejectTransaction(ModelTest):
    """TakeProfitOrderRejectTransaction unit test stubs"""

    class Factory(MockFactory[TakeProfitOrderRejectTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
