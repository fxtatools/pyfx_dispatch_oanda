
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.list_transactions200_response import ListTransactions200Response


class TestListTransactions200Response(ModelTest):
    """ListTransactions200Response unit test stubs"""

    class Factory(MockFactory[ListTransactions200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
