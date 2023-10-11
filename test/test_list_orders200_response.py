
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.list_orders200_response import ListOrders200Response


class TestListOrders200Response(ModelTest):
    """ListOrders200Response unit test stubs"""

    class Factory(MockFactory[ListOrders200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
