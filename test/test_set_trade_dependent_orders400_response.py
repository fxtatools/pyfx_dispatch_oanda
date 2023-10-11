
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.set_trade_dependent_orders400_response import SetTradeDependentOrders400Response


class TestSetTradeDependentOrders400Response(ModelTest):
    """SetTradeDependentOrders400Response unit test stubs"""

    class Factory(MockFactory[SetTradeDependentOrders400Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
