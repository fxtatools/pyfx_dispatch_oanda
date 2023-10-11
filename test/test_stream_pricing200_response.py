
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.stream_pricing200_response import StreamPricing200Response


class TestStreamPricing200Response(ModelTest):
    """StreamPricing200Response unit test stubs"""

    class Factory(MockFactory[StreamPricing200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
