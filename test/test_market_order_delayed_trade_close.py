
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.market_order_delayed_trade_close import MarketOrderDelayedTradeClose


class TestMarketOrderDelayedTradeClose(ModelTest):
    """MarketOrderDelayedTradeClose unit test stubs"""

    class Factory(MockFactory[MarketOrderDelayedTradeClose]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
