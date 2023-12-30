"""Request dispatch for GetAccount200Response"""

from typing import Annotated, Mapping
from typing_extensions import ClassVar

from ...util.singular_map import SingularMap

from ..request_base import ApiRestRequest
from ...models.get_account_summary200_response import GetAccountSummary200Response
from ...models.account_summary import AccountSummary
from ...request_constants import RequestMethod
from ...transport.account_id import AccountId

from ...transport.data import ApiClass
from ...api.param_info import path_param


class GetAccountSummaryRequest(ApiRestRequest[GetAccountSummary200Response, AccountSummary]):
    """Fetch account summary information"""

    request_method: ClassVar[RequestMethod] = RequestMethod.GET
    request_path: ClassVar[str] = '/accounts/{accountID}/summary'
    response_types: Mapping[int, ApiClass] = SingularMap(200, GetAccountSummary200Response)

    #
    # path params
    #
    account_id: Annotated[AccountId, path_param(..., alias="accountID")]


__all__ = ("GetAccountRequest",)
