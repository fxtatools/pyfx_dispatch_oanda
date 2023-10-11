
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.order_client_extensions_modify_transaction import OrderClientExtensionsModifyTransaction


class TestOrderClientExtensionsModifyTransaction(ModelTest):
    """OrderClientExtensionsModifyTransaction unit test stubs"""

    class Factory(MockFactory[OrderClientExtensionsModifyTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
