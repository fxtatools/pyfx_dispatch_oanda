
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.get_transaction200_response import GetTransaction200Response


class TestGetTransaction200Response(ModelTest):
    """GetTransaction200Response unit test stubs"""

    class Factory(MockFactory[GetTransaction200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
