
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.order_book import OrderBook


class TestOrderBook(ModelTest):
    """OrderBook unit test stubs"""

    class Factory(MockFactory[OrderBook]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
