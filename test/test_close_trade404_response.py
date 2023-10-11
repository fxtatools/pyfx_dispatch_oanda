
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.close_trade404_response import CloseTrade404Response


class TestCloseTrade404Response(ModelTest):
    """CloseTrade404Response unit test stubs"""

    class Factory(MockFactory[CloseTrade404Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
