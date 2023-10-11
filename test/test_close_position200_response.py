
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.close_position200_response import ClosePosition200Response


class TestClosePosition200Response(ModelTest):
    """ClosePosition200Response unit test stubs"""

    class Factory(MockFactory[ClosePosition200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
