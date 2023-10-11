
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.get_account200_response import GetAccount200Response


class TestGetAccount200Response(ModelTest):
    """GetAccount200Response unit test stubs"""

    class Factory(MockFactory[GetAccount200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
