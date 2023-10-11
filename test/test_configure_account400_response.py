
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.configure_account400_response import ConfigureAccount400Response


class TestConfigureAccount400Response(ModelTest):
    """ConfigureAccount400Response unit test stubs"""

    class Factory(MockFactory[ConfigureAccount400Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
