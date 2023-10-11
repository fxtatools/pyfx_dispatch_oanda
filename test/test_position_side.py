
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.position_side import PositionSide


class TestPositionSide(ModelTest):
    """PositionSide unit test stubs"""

    class Factory(MockFactory[PositionSide]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
