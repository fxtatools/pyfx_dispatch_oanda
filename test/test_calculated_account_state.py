
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.calculated_account_state import CalculatedAccountState


class TestCalculatedAccountState(ModelTest):
    """CalculatedAccountState unit test stubs"""

    class Factory(MockFactory[CalculatedAccountState]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
