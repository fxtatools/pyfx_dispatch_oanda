"""Request dispatch for ListAccounts200Response"""

from typing import Iterator, Mapping
from typing_extensions import ClassVar

from ...util.singular_map import SingularMap

from ..request_base import ApiRestRequest
from ...models.list_accounts200_response import ListAccounts200Response
from ...models.account_properties import AccountProperties
from ...request_constants import RequestMethod

from ...transport.data import ApiClass

class ListAcccountsRequest(ApiRestRequest[ListAccounts200Response, AccountProperties]):

    request_method: ClassVar[RequestMethod] = RequestMethod.GET
    request_path: ClassVar[str] = '/accounts'
    response_types: Mapping[int, ApiClass] = SingularMap(200, ListAccounts200Response)

    @classmethod
    def response_iter(cls, response: ListAccounts200Response) -> Iterator[AccountProperties]:
        return response.accounts


__all__ = ("ListAcccountsRequest",)
