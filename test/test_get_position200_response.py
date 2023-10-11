
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.get_position200_response import GetPosition200Response


class TestGetPosition200Response(ModelTest):
    """GetPosition200Response unit test stubs"""

    class Factory(MockFactory[GetPosition200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
