
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.margin_call_extend_transaction import MarginCallExtendTransaction


class TestMarginCallExtendTransaction(ModelTest):
    """MarginCallExtendTransaction unit test stubs"""

    class Factory(MockFactory[MarginCallExtendTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
