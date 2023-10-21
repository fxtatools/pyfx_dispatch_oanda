"""Unit test definition for pyfx.dispatch.oanda"""
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.account import Account


class TestAccount(ModelTest):
    """Account unit test stubs"""

    class Factory(MockFactory[Account]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
