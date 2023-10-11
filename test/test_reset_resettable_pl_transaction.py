
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.reset_resettable_pl_transaction import ResetResettablePLTransaction


class TestResetResettablePLTransaction(ModelTest):
    """ResetResettablePLTransaction unit test stubs"""

    class Factory(MockFactory[ResetResettablePLTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
