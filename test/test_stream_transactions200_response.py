
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.stream_transactions200_response import StreamTransactions200Response


class TestStreamTransactions200Response(ModelTest):
    """StreamTransactions200Response unit test stubs"""

    class Factory(MockFactory[StreamTransactions200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
