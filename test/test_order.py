"""Unit test definition for the abstract Order class"""

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.order import Order


class TestOrder(ModelTest):
    """Order unit test stubs"""

    class Factory(MockFactory[Order]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
