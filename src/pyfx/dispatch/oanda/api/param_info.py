"""Parameter definition classes for the API requests model"""

from typing import Optional
from pyfx.dispatch.oanda.transport.data import JsonTypesRepository, TransportModelRepository
from pyfx.dispatch.oanda.transport.transport_base import TransportFieldInfo, TransportType, TransportTypeInfer


#
# Request Parameter Definitions - Base Classes
#


class ParamInfo(TransportFieldInfo):

    @classmethod
    def get_types_repository(cls) -> TransportModelRepository:
        return JsonTypesRepository

    @classmethod
    def from_field(cls, default, transport_type: TransportType = TransportTypeInfer, **kw):
        return super().from_field(default, transport_type=transport_type, **kw)


class UrlParamInfo(ParamInfo):
    pass


#
# Path Params
#


class PathParamInfo(UrlParamInfo):
    pass


def path_param(default, alias: Optional[str] = None, **kw):
    return PathParamInfo.from_field(default, alias=alias, **kw)

#
# Query Params
#


class QueryParamInfo(UrlParamInfo):
    pass


def query_param(default, alias: Optional[str] = None, **kw):
    return QueryParamInfo.from_field(default, alias=alias, **kw)


__all__ = "ParamInfo", "UrlParamInfo", "PathParamInfo", "path_param", "QueryParamInfo", "query_param"
