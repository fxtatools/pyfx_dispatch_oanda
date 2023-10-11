
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.set_order_client_extensions200_response import SetOrderClientExtensions200Response


class TestSetOrderClientExtensions200Response(ModelTest):
    """SetOrderClientExtensions200Response unit test stubs"""

    class Factory(MockFactory[SetOrderClientExtensions200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
