
"""Unit test definition for pyfx.dispatch.oanda"""


from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.create_order400_response import CreateOrder400Response


class TestCreateOrder400Response(ModelTest):
    """CreateOrder400Response unit test stubs"""

    class Factory(MockFactory[CreateOrder400Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
