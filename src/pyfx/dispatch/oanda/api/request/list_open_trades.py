"""Request dispatch for ListOpenTrades200Response"""

from collections.abc import Iterator, Mapping
from typing import Annotated, Mapping
from typing_extensions import ClassVar

from ...util.singular_map import SingularMap

from ...api.request_base import ApiRestRequest
from ...models.list_open_trades200_response import ListOpenTrades200Response
from ...models.trade import Trade
from ...request_constants import RequestMethod
from ...transport.data import ApiClass
from ...api.param_info import path_param

from ...models.common_types import AccountId


class ListOpenTradesRequest(ApiRestRequest[ListOpenTrades200Response, Trade]):
    request_method: ClassVar[RequestMethod] = RequestMethod.GET
    request_path: ClassVar[str] = '/accounts/{accountID}/openTrades'
    response_types: ClassVar[Mapping[int, ApiClass]] = SingularMap(200, ListOpenTrades200Response)

    ## path parameters
    account_id: Annotated[AccountId, path_param(..., alias="accountID")]

    @classmethod
    def response_iter(cls, response: ListOpenTrades200Response) -> Iterator[Trade]:
        return response.trades


__all__ = ("ListOpenTradesRequest",)
