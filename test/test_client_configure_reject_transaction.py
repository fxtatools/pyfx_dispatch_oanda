
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.client_configure_reject_transaction import ClientConfigureRejectTransaction


class TestClientConfigureRejectTransaction(ModelTest):
    """ClientConfigureRejectTransaction unit test stubs"""

    class Factory(MockFactory[ClientConfigureRejectTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
