
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.client_price import ClientPrice


class TestClientPrice(ModelTest):
    """ClientPrice unit test stubs"""

    class Factory(MockFactory[ClientPrice]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
