
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.client_configure_transaction import ClientConfigureTransaction


class TestClientConfigureTransaction(ModelTest):
    """ClientConfigureTransaction unit test stubs"""

    class Factory(MockFactory[ClientConfigureTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
