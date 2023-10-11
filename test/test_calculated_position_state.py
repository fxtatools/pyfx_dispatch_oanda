
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.calculated_position_state import CalculatedPositionState


class TestCalculatedPositionState(ModelTest):
    """CalculatedPositionState unit test stubs"""

    class Factory(MockFactory[CalculatedPositionState]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
