
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.close_trade400_response import CloseTrade400Response


class TestCloseTrade400Response(ModelTest):
    """CloseTrade400Response unit test stubs"""

    class Factory(MockFactory[CloseTrade400Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
