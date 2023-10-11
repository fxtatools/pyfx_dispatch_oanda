
"""Unit test definition for pyfx.dispatch.oanda"""
from pyfx.dispatch.oanda.models  import GetAccountInstruments200Response
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests

class TestGetAccountInstruments200Response(ModelTest):
    """unit tests for GetAccountInstruments200Response"""

    class Factory(MockFactory[GetAccountInstruments200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
