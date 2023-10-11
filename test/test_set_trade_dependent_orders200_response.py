
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.set_trade_dependent_orders200_response import SetTradeDependentOrders200Response


class TestSetTradeDependentOrders200Response(ModelTest):
    """SetTradeDependentOrders200Response unit test stubs"""

    class Factory(MockFactory[SetTradeDependentOrders200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
