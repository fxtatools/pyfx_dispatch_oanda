
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.transfer_funds_reject_transaction import TransferFundsRejectTransaction


class TestTransferFundsRejectTransaction(ModelTest):
    """TransferFundsRejectTransaction unit test stubs"""

    class Factory(MockFactory[TransferFundsRejectTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
