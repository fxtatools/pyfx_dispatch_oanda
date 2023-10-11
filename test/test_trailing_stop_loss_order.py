
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.trailing_stop_loss_order import TrailingStopLossOrder


class TestTrailingStopLossOrder(ModelTest):
    """TrailingStopLossOrder unit test stubs"""

    class Factory(MockFactory[TrailingStopLossOrder]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
