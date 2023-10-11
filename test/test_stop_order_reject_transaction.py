
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.stop_order_reject_transaction import StopOrderRejectTransaction


class TestStopOrderRejectTransaction(ModelTest):
    """StopOrderRejectTransaction unit test stubs"""

    class Factory(MockFactory[StopOrderRejectTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
