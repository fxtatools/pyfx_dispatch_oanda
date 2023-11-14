"""Unit test definition for SetTradeDependentOrdersRequest"""

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.set_trade_dependent_orders_request import SetTradeDependentOrdersRequest


class TestSetTradeDependentOrdersRequest(ModelTest):
    """SetTradeDependentOrdersRequest unit test stubs"""

    class Factory(MockFactory[SetTradeDependentOrdersRequest]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
