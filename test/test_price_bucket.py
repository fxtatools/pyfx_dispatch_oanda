
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.price_bucket import PriceBucket


class TestPriceBucket(ModelTest):
    """PriceBucket unit test stubs"""

    class Factory(MockFactory[PriceBucket]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
