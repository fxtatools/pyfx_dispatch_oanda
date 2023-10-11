
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.get_instrument_price200_response import GetInstrumentPrice200Response


class TestGetInstrumentPrice200Response(ModelTest):
    """GetInstrumentPrice200Response unit test stubs"""

    class Factory(MockFactory[GetInstrumentPrice200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
