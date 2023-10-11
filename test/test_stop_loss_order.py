
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.stop_loss_order import StopLossOrder


class TestStopLossOrder(ModelTest):
    """StopLossOrder unit test stubs"""

    class Factory(MockFactory[StopLossOrder]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
