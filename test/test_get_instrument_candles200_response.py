
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.get_instrument_candles200_response import GetInstrumentCandles200Response


class TestGetInstrumentCandles200Response(ModelTest):
    """GetInstrumentCandles200Response unit test stubs"""

    class Factory(MockFactory[GetInstrumentCandles200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
