
"""Unit test definition for pyfx.dispatch.oanda"""

from typing import Any

from pyfx.dispatch.oanda.test import MockFactory, ModelTest, run_tests
from pyfx.dispatch.oanda.models.get_account_summary200_response import GetAccountSummary200Response

## simply importing either of the following produces an odd side effect for polyfactory.
## it produces some sort of a side effect, in effect mangling the existing
## factory configuration for the class
#
# from pyfx.dispatch.oanda.models import AccountSummary
#
# from test_account_summary import TestAccountSummary

class TestGetAccountSummary200Response(ModelTest):
    """GetAccountSummary200Response unit test stubs"""

    class Factory(MockFactory[GetAccountSummary200Response]):
        pass
    
    __factory__ = Factory


if __name__ == '__main__':
    run_tests(__file__)
