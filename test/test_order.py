
"""Unit test definition for pyfx.dispatch.oanda"""


from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.market_order import MarketOrder


class TestOrder(ModelTest):
    """Order unit test stubs"""

    class Factory(MockFactory[MarketOrder]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
