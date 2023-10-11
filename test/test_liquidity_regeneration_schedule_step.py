
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.liquidity_regeneration_schedule_step import LiquidityRegenerationScheduleStep


class TestLiquidityRegenerationScheduleStep(ModelTest):
    """LiquidityRegenerationScheduleStep unit test stubs"""

    class Factory(MockFactory[LiquidityRegenerationScheduleStep]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
