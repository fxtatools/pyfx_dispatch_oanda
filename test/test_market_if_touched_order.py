
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.market_if_touched_order import MarketIfTouchedOrder


class TestMarketIfTouchedOrder(ModelTest):
    """MarketIfTouchedOrder unit test stubs"""

    class Factory(MockFactory[MarketIfTouchedOrder]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
