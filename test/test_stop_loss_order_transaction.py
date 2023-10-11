
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.stop_loss_order_transaction import StopLossOrderTransaction


class TestStopLossOrderTransaction(ModelTest):
    """StopLossOrderTransaction unit test stubs"""

    class Factory(MockFactory[StopLossOrderTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
