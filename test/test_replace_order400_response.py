
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.replace_order400_response import ReplaceOrder400Response


class TestReplaceOrder400Response(ModelTest):
    """ReplaceOrder400Response unit test stubs"""

    class Factory(MockFactory[ReplaceOrder400Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
