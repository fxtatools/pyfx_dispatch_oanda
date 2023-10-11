
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.account_changes_state import AccountChangesState


class TestAccountChangesState(ModelTest):
    """AccountChangesState unit test stubs"""

    class Factory(MockFactory[AccountChangesState]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
