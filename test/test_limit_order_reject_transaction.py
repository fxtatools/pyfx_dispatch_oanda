
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.limit_order_reject_transaction import LimitOrderRejectTransaction


class TestLimitOrderRejectTransaction(ModelTest):
    """LimitOrderRejectTransaction unit test stubs"""

    class Factory(MockFactory[LimitOrderRejectTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
