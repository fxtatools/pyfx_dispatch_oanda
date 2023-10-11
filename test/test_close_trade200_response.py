
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.close_trade200_response import CloseTrade200Response


class TestCloseTrade200Response(ModelTest):
    """CloseTrade200Response unit test stubs"""

    class Factory(MockFactory[CloseTrade200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
