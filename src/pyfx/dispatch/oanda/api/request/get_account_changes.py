"""Request dispatch for GetAccount200Response"""

from typing import Annotated, Mapping, Optional
from typing_extensions import ClassVar
from pyfx.dispatch.oanda.transport.account_id import AccountId

from pyfx.dispatch.oanda.models.common_types import TransactionId

from ...util.singular_map import SingularMap

from ..request_base import ApiRestRequest
from ...models.get_account_changes200_response import GetAccountChanges200Response
from ...models.account import Account
from ...request_constants import RequestMethod

from ...transport.data import ApiClass
from ...api.param_info import path_param, query_param


class GetAccountSummaryRequest(ApiRestRequest[GetAccountChanges200Response, Account]):
    """Fetch details for changes in orders, trades, positions, and transactions
    since some transaction ID
    """

    request_method: ClassVar[RequestMethod] = RequestMethod.GET
    request_path: ClassVar[str] = '/accounts/{accountID}/summary'
    response_types: Mapping[int, ApiClass] = SingularMap(200, GetAccountChanges200Response)

    # path params
    account_id: Annotated[AccountId, path_param(..., alias="accountID")]

    # query params
    since_transaction_id = Annotated[Optional[TransactionId], query_param(None, alias="sinceTransactionID")]


__all__ = ("GetAccountSummaryRequest",)
