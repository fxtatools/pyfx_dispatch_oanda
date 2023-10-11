
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.instruments_instrument_position_book_get200_response import InstrumentsInstrumentPositionBookGet200Response


class TestInstrumentsInstrumentPositionBookGet200Response(ModelTest):
    """InstrumentsInstrumentPositionBookGet200Response unit test stubs"""

    class Factory(MockFactory[InstrumentsInstrumentPositionBookGet200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
