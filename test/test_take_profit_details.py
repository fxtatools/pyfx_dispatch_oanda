
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.take_profit_details import TakeProfitDetails


class TestTakeProfitDetails(ModelTest):
    """TakeProfitDetails unit test stubs"""

    class Factory(MockFactory[TakeProfitDetails]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
