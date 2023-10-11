
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.candlestick_data import CandlestickData


class TestCandlestickData(ModelTest):
    """CandlestickData unit test stubs"""

    class Factory(MockFactory[CandlestickData]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
