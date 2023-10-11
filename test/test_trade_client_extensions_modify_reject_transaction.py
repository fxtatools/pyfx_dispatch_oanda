
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.trade_client_extensions_modify_reject_transaction import TradeClientExtensionsModifyRejectTransaction


class TestTradeClientExtensionsModifyRejectTransaction(ModelTest):
    """TradeClientExtensionsModifyRejectTransaction unit test stubs"""

    class Factory(MockFactory[TradeClientExtensionsModifyRejectTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
