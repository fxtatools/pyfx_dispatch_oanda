"""Unit test definition for StopLossDetails"""

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.stop_loss_details import StopLossDetails


class TestStopLossDetails(ModelTest):
    """StopLossDetails unit test stubs"""

    class Factory(MockFactory[StopLossDetails]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
