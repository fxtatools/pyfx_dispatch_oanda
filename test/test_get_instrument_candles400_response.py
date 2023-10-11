
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.get_instrument_candles400_response import FxTrade400Response


class TestGetInstrumentCandles400Response(ModelTest):
    """GetInstrumentCandles400Response unit test stubs"""

    class Factory(MockFactory[FxTrade400Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
