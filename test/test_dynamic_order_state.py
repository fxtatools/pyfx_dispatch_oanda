
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.dynamic_order_state import DynamicOrderState


class TestDynamicOrderState(ModelTest):
    """DynamicOrderState unit test stubs"""

    class Factory(MockFactory[DynamicOrderState]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
