
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.market_if_touched_order_transaction import MarketIfTouchedOrderTransaction


class TestMarketIfTouchedOrderTransaction(ModelTest):
    """MarketIfTouchedOrderTransaction unit test stubs"""

    class Factory(MockFactory[MarketIfTouchedOrderTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
