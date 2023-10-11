
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.trade_summary import TradeSummary


class TestTradeSummary(ModelTest):
    """TradeSummary unit test stubs"""

    class Factory(MockFactory[TradeSummary]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
