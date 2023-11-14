"""Request dispatch for ListTrades200Response"""

from collections.abc import Mapping
from typing import Annotated, Iterator, Mapping, Optional, Sequence
from typing_extensions import ClassVar

from ...util.singular_map import SingularMap

from ...api.request_base import ApiLinkedRequest
from ...models.list_trades200_response import ListTrades200Response
from ...models.trade import Trade
from ...request_constants import RequestMethod
from ...transport.data import ApiClass
from ...api.param_info import path_param, query_param

from ...models.common_types import AccountId, InstrumentName, TradeId
from ...models.trade_state_filter import TradeStateFilter


class ListTradesRequest(ApiLinkedRequest[ListTrades200Response, Trade]):
    request_method: ClassVar[RequestMethod] = RequestMethod.GET
    request_path: ClassVar[str] = '/accounts/{accountID}/trades'
    response_types: ClassVar[Mapping[int, ApiClass]] = SingularMap(200, ListTrades200Response)

    ## path parameterse
    account_id: Annotated[AccountId, path_param(..., alias="accountID")]
    ## query parameters
    ids: Annotated[Optional[Sequence[TradeId]], query_param(None)]
    state: Annotated[Optional[TradeStateFilter], query_param(TradeStateFilter.OPEN)]
    instrument: Annotated[Optional[InstrumentName], query_param(None)]
    count: Annotated[Optional[int], query_param(50, max=500)]
    before_id: Annotated[Optional[TradeId], query_param(None, alias="beforeID")]

    @classmethod
    def response_iter(cls, response: ListTrades200Response) -> Iterator[Trade]:
        return response.trades


__all__ = ("ListTradesRequest",)
