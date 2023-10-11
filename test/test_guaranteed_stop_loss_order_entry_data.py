
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.guaranteed_stop_loss_order_entry_data import GuaranteedStopLossOrderEntryData


class TestGuaranteedStopLossOrderEntryData(ModelTest):
    """GuaranteedStopLossOrderEntryData unit test stubs"""

    class Factory(MockFactory[GuaranteedStopLossOrderEntryData]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
