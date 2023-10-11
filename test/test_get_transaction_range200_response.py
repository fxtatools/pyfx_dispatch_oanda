
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.get_transaction_range200_response import GetTransactionRange200Response


class TestGetTransactionRange200Response(ModelTest):
    """GetTransactionRange200Response unit test stubs"""

    class Factory(MockFactory[GetTransactionRange200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
