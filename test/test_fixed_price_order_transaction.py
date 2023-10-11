
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.fixed_price_order_transaction import FixedPriceOrderTransaction


class TestFixedPriceOrderTransaction(ModelTest):
    """FixedPriceOrderTransaction unit test stubs"""

    class Factory(MockFactory[FixedPriceOrderTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
