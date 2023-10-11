
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.replace_order404_response import ReplaceOrder404Response


class TestReplaceOrder404Response(ModelTest):
    """ReplaceOrder404Response unit test stubs"""

    class Factory(MockFactory[ReplaceOrder404Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
