
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.get_order200_response import GetOrder200Response


class TestGetOrder200Response(ModelTest):
    """GetOrder200Response unit test stubs"""

    class Factory(MockFactory[GetOrder200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
