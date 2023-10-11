
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.trailing_stop_loss_order_request import TrailingStopLossOrderRequest


class TestTrailingStopLossOrderRequest(ModelTest):
    """TrailingStopLossOrderRequest unit test stubs"""

    class Factory(MockFactory[TrailingStopLossOrderRequest]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
