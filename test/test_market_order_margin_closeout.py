
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.market_order_margin_closeout import MarketOrderMarginCloseout


class TestMarketOrderMarginCloseout(ModelTest):
    """MarketOrderMarginCloseout unit test stubs"""

    class Factory(MockFactory[MarketOrderMarginCloseout]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
