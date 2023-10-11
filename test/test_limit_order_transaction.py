
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.limit_order_transaction import LimitOrderTransaction


class TestLimitOrderTransaction(ModelTest):
    """LimitOrderTransaction unit test stubs"""

    class Factory(MockFactory[LimitOrderTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
