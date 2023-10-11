"""Unit test definition for pyfx.dispatch.oanda"""

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models import MarketOrderTransaction


class TestTransaction(ModelTest):
    """Transaction unit test stubs"""

    class Factory(MockFactory[MarketOrderTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
