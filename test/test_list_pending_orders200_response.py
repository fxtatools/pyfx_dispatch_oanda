
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.list_pending_orders200_response import ListPendingOrders200Response


class TestListPendingOrders200Response(ModelTest):
    """ListPendingOrders200Response unit test stubs"""

    class Factory(MockFactory[ListPendingOrders200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
