
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.stop_loss_order_reject_transaction import StopLossOrderRejectTransaction


class TestStopLossOrderRejectTransaction(ModelTest):
    """StopLossOrderRejectTransaction unit test stubs"""

    class Factory(MockFactory[StopLossOrderRejectTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
