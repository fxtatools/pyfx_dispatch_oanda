
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.margin_call_enter_transaction import MarginCallEnterTransaction


class TestMarginCallEnterTransaction(ModelTest):
    """MarginCallEnterTransaction unit test stubs"""

    class Factory(MockFactory[MarginCallEnterTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
