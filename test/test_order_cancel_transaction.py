
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.order_cancel_transaction import OrderCancelTransaction


class TestOrderCancelTransaction(ModelTest):
    """OrderCancelTransaction unit test stubs"""

    class Factory(MockFactory[OrderCancelTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
