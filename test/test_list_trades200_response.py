
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.list_trades200_response import ListTrades200Response


class TestListTrades200Response(ModelTest):
    """ListTrades200Response unit test stubs"""

    class Factory(MockFactory[ListTrades200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
