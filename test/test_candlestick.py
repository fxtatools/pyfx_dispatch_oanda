
"""Unit test definition for pyfx.dispatch.oanda"""

from assertpy import assert_that

import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.candlestick import Candlestick


class TestCandlestick(ModelTest):
    """Candlestick unit test stubs"""

    class Factory(MockFactory[Candlestick]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
