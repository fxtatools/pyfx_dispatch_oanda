
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.create_order404_response import CreateOrder404Response


class TestCreateOrder404Response(ModelTest):
    """CreateOrder404Response unit test stubs"""

    class Factory(MockFactory[CreateOrder404Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
