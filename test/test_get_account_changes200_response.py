"""Unit test definition for TestGetAccountChanges200Response"""

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.get_account_changes200_response import GetAccountChanges200Response


class TestGetAccountChanges200Response(ModelTest):
    """GetAccountChanges200Response unit test stubs"""

    class Factory(MockFactory[GetAccountChanges200Response]):
        pass

    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
