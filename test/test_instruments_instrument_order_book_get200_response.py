
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.instruments_instrument_order_book_get200_response import InstrumentsInstrumentOrderBookGet200Response


class TestInstrumentsInstrumentOrderBookGet200Response(ModelTest):
    """InstrumentsInstrumentOrderBookGet200Response unit test stubs"""

    class Factory(MockFactory[InstrumentsInstrumentOrderBookGet200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
