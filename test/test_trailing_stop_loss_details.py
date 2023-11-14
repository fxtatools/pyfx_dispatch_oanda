"""Unit test definition for TrailingStopLossDetails"""

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.trailing_stop_loss_details import TrailingStopLossDetails


class TestTrailingStopLossDetails(ModelTest):
    """TrailingStopLossDetails unit test stubs"""

    class Factory(MockFactory[TrailingStopLossDetails]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
