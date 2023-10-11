
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.fixed_price_order import FixedPriceOrder


class TestFixedPriceOrder(ModelTest):
    """FixedPriceOrder unit test stubs"""

    class Factory(MockFactory[FixedPriceOrder]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
