
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.stop_order_transaction import StopOrderTransaction


class TestStopOrderTransaction(ModelTest):
    """StopOrderTransaction unit test stubs"""

    class Factory(MockFactory[StopOrderTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
