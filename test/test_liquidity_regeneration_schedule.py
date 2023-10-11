
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.liquidity_regeneration_schedule import LiquidityRegenerationSchedule


class TestLiquidityRegenerationSchedule(ModelTest):
    """LiquidityRegenerationSchedule unit test stubs"""

    class Factory(MockFactory[LiquidityRegenerationSchedule]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
