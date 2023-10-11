
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.transfer_funds_transaction import TransferFundsTransaction


class TestTransferFundsTransaction(ModelTest):
    """TransferFundsTransaction unit test stubs"""

    class Factory(MockFactory[TransferFundsTransaction]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
