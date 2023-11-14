
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.account_properties import AccountProperties


from assertpy import assert_that  # type: ignore[import-untyped]

class TestAccountProperties(ModelTest):
    """AccountProperties unit test stubs"""

    class Factory(MockFactory[AccountProperties]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
