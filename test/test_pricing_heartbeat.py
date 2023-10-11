
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.pricing_heartbeat import PricingHeartbeat


class TestPricingHeartbeat(ModelTest):
    """PricingHeartbeat unit test stubs"""

    class Factory(MockFactory[PricingHeartbeat]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
