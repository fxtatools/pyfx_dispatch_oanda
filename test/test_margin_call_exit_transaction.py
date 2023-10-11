
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.margin_call_exit_transaction import MarginCallExitTransaction


class TestMarginCallExitTransaction(ModelTest):
    """MarginCallExitTransaction unit test stubs"""

    class Factory(MockFactory[MarginCallExitTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
