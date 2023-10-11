
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.market_order_position_closeout import MarketOrderPositionCloseout


class TestMarketOrderPositionCloseout(ModelTest):
    """MarketOrderPositionCloseout unit test stubs"""

    class Factory(MockFactory[MarketOrderPositionCloseout]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
