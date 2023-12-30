"""Request dispatch for GetAccount200Response"""

from typing import Annotated, Mapping
from typing_extensions import ClassVar

from pyfx.dispatch.oanda.transport.account_id import AccountId

from ...util.singular_map import SingularMap

from ..request_base import ApiRestRequest
from ...models.get_account200_response import GetAccount200Response
from ...models.account import Account
from ...request_constants import RequestMethod

from ...transport.data import ApiClass
from ...api.param_info import path_param


class GetAccountRequest(ApiRestRequest[GetAccount200Response, Account]):
    """Fetch information for account trades, positions, and orders
    """

    request_method: ClassVar[RequestMethod] = RequestMethod.GET
    request_path: ClassVar[str] = '/accounts/{accountID}'
    response_types: Mapping[int, ApiClass] = SingularMap(200, GetAccount200Response)

    # path params
    account_id: Annotated[AccountId, path_param(..., alias="accountID")]


__all__ = ("GetAccountRequest",)
