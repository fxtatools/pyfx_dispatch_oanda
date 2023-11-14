"""Request dispatch for GetAccountInstruments200Response"""

from collections.abc import Iterator
from typing import Annotated, Optional, Mapping
from typing_extensions import ClassVar, TypeVar

from ..request_base import ApiRestRequest
from ...models.get_account_instruments200_response import GetAccountInstruments200Response
from ...models.instrument import Instrument
from ...request_constants import RequestMethod

from ...transport.data import ApiClass
from ...api.param_info import path_param, query_param
from ...models.common_types import AccountId, InstrumentName
from ...util.singular_map import SingularMap


T_co = TypeVar("T_co")
T_result = TypeVar("T_result")


class GetAccountInstrumentsRequest(ApiRestRequest[GetAccountInstruments200Response, Instrument]):

    request_method: ClassVar[RequestMethod] = RequestMethod.GET
    request_path: ClassVar[str] = '/accounts/{accountID}/instruments'
    response_types: Mapping[int, ApiClass] = SingularMap(200, GetAccountInstruments200Response)

    account_id: Annotated[AccountId, path_param(..., alias="accountID")]

    instruments: Annotated[Optional[list[InstrumentName]], query_param(None)]

    @classmethod
    def response_iter(cls, response: GetAccountInstruments200Response) -> Iterator[Instrument]:
        return response.instruments


__all__ = ("GetAccountInstrumentsRequest",)
