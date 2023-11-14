
"""Unit test definition for pyfx.dispatch.oanda"""


import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.list_accounts200_response import ListAccounts200Response


from assertpy import assert_that  # type: ignore[import-untyped]

class TestListAccounts200Response(ModelTest):
    """ListAccounts200Response unit test stubs"""

    class Factory(MockFactory[ListAccounts200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
