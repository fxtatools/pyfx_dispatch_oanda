
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.trailing_stop_loss_order_reject_transaction import TrailingStopLossOrderRejectTransaction


class TestTrailingStopLossOrderRejectTransaction(ModelTest):
    """TrailingStopLossOrderRejectTransaction unit test stubs"""

    class Factory(MockFactory[TrailingStopLossOrderRejectTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
