"""Unit test definition for the abstract Transaction class"""

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.transaction import Transaction


class TestTransaction(ModelTest):
    """Transaction unit test stubs"""

    class Factory(MockFactory[Transaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
