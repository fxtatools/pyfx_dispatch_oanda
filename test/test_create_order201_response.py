
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.create_order201_response import CreateOrder201Response


class TestCreateOrder201Response(ModelTest):
    """CreateOrder201Response unit test stubs"""

    class Factory(MockFactory[CreateOrder201Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
