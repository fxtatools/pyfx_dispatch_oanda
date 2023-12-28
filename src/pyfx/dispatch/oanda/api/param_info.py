"""Parameter definition classes for the API requests model"""

from abc import ABC
from datetime import datetime
import click
from collections.abc import Callable, Sequence
from enum import Enum
from click.core import Context, Parameter
from immutables import Map
import inspect
import os
from pandas import Timestamp
from numpy import double, datetime64
from pydantic.fields import PydanticUndefined
from types import new_class
from typing import TYPE_CHECKING, Any, Generic, Mapping, Optional, Union
from typing_extensions import ClassVar, Self, TypeVar, TypeAlias

from pyfx.dispatch.oanda.transport.data import (
    JsonTypesRepository, TransportModelRepository
)
from pyfx.dispatch.oanda.transport.transport_base import (
    TransportEnumType, TransportInterface, TransportType, TransportTypeInfer,
    TransportStr,  TransportIntStr,  TransportFloatStr,
    TransportBool, TransportEnum, TransportFieldInfo,
    TransportInt, TransportTimestamp, TransportValuesType,
    TransportNone, TransportEnumStrType, TransportTypeClass,
    TransportInterfaceClass, TRANSPORT_VALUES_STORAGE_CLASS
)
from pyfx.dispatch.oanda.models.common_types import (
    InstrumentName, AccountUnits, FloatValue, PriceValue, LotsValue,
    TradeId, TransactionId, OrderId, Time
)

from pyfx.dispatch.oanda.transport.repository import TransportBaseRepository
from pyfx.dispatch.oanda.mapped_enum import MappedEnum



#
# Request Parameter Definitions - Base Classes
#


Ti = TypeVar("Ti")
To = TypeVar("To")

#
# Click support
#

T_info = TypeVar("T_info", bound="ParamInfo")


class ModelParam(click.Parameter, Generic[T_info]):
    # note callback: Callable[[context:click.Context, param: RequestParam, value: Any], Any]
    #
    # primary usage: .request_base :: RequestCommand / RequestContext
    #
    if TYPE_CHECKING:
        field_info: T_info

    def get_description(self):
        desc = self.field_info.description

    def get_help_record(self, ctx: Context) -> Optional[tuple[str, str]]:
        ## add default value information to the help string, when avaialble
        hrec  = super().get_help_record(ctx)
        if hrec:
            name, desc = hrec
            info = self.field_info
            field_desc = info.description
            new_para = False
            if field_desc:
                desc = desc + os.linesep +  inspect.cleandoc(field_desc)
                new_para = True
            default = info.get_default()
            if default is not PydanticUndefined:
                txtyp: ParamInterface = info.transport_type
                if issubclass(txtyp, ParamEnum):
                    scls: MappedEnum = txtyp.storage_class
                    mmap = scls._member_map_
                    if new_para:
                        desc = desc + os.linesep * 2
                        new_para = False
                    choices_str = "choices: " + ", ".join(mmap[name].value for name in scls._member_names_)
                    desc = desc + choices_str + (os.linesep * 2)
                if issubclass(txtyp, TransportBool):
                    # presenting one of "--<arg_stem>" or "--no-<arg_stem>"
                    # per the the default value
                    if default is not None:
                        s_default = self.opts[0] if default else self.secondary_opts[0]
                elif default is None:
                    s_default = "None"
                else:
                    s_default = txtyp.unparse_py(default)
                    if not isinstance(s_default, str):
                        s_default = str(s_default)
                desc = desc + "[default: " + s_default + "]"
            return name, desc


class RequestArg(ModelParam, click.Argument):
    pass


class RequestOpt(ModelParam, click.Option):
    pass


#
# Param model
#

ParseCallback: TypeAlias = Callable[[Union[Ti, To], Self], Ti]

class ParamInfo(TransportFieldInfo, Generic[Ti, To]):
    if TYPE_CHECKING:
        transport_type: ClassVar["ParamInterface[Ti, To]"]
        click_param: click.Parameter
        parse: Optional[ParseCallback] = None ## FIXME apply when provided

    @classmethod
    def get_types_repository(cls) -> TransportModelRepository:
        return JsonTypesRepository

    @classmethod
    def from_field(cls, default,
                   transport_type: TransportType = TransportTypeInfer,
                   parse: Optional[ParseCallback] = None,
                   **kw):
        info = super().from_field(default, transport_type=transport_type, **kw)
        if parse:
            info.parse = parse
        return info

    def parse_input(self, value: Union[Ti, To], context: Optional[click.Context] = None) -> To:
        if hasattr(self, "parse"):
            return self.parse(value, self)
        else:
            return self.transport_type.parse_arg(value, context)

    def to_click_param(self) -> click.Parameter:
        # usage: see ApiRequest.get_click_command()
        if hasattr(self, "click_param"):
            return self.click_param
        else:
            name = self.name
            txtyp = self.transport_type
            info_default = self.default
            default = None if info_default is PydanticUndefined else self.get_default
            required = info_default is PydanticUndefined
            restargs = dict()

            if required is True:
                arg = name
            elif issubclass(txtyp, TransportBool):
                ## https://click.palletsprojects.com/en/8.1.x/options/#boolean-flags
                dashname = name.replace("_", "-")
                arg = "--" + dashname + "/--no-" + dashname
                if required is False:
                    ## arg is available in click.Option
                    restargs["is_flag"] = True
            else:
                arg = "--" + name.replace("_", "-")
            args = (arg,)

            if issubclass(txtyp, TransportValuesType):
                nargs = -1
            elif required is True:
                nargs=1
            else:
                nargs=1

            metavar = name

            param_cls = RequestArg if required is True else RequestOpt

            param = param_cls(
                args,

                type=txtyp.get_click_param_type(self),
                required=required,

                nargs=nargs,
                metavar=metavar,
                **restargs
            )
            param.field_info = self ## FIXME use this extension field during help formatting
            self.click_param = param
            return param


class UrlParamInfo(ParamInfo):
    pass


#
# Path Params
#


class PathParamInfo(UrlParamInfo):
    pass


def path_param(default, alias: Optional[str] = None, description: Optional[str] = None, **kw):
    return PathParamInfo.from_field(default, alias=alias, description=description, **kw)

#
# Query Params
#


class QueryParamInfo(UrlParamInfo):
    pass


def query_param(default, alias: Optional[str] = None, description: Optional[str] = None, **kw):
    return QueryParamInfo.from_field(default, alias=alias, description=description, **kw)



class ParamInterface(TransportInterface[Ti, To], metaclass=TransportInterfaceClass):
    @classmethod
    def get_click_param_type(cls, info: ParamInfo):
        return ParamInterfaceType(cls, info)

    @classmethod
    def parse_arg(cls, arg: Union[str, Ti], context: click.Context) -> Ti:
        if arg.__class__ is str:
            return cls.parse(arg)
        else:
            return arg



class ParamInterfaceType(click.ParamType):
    #
    # an interface onto click.ParamType
    #

    if TYPE_CHECKING:
        param_interface: type[ParamInterface]
        field_info: ParamInfo

    def __init__(self, interface: type[ParamInterface], info: ParamInfo):
        self.param_interface = interface
        self.name = interface.__name__
        self.field_info = info

    def to_info_dict(self) -> Mapping[str, Any]:
        txtyp: type[ParamInterface] = self.param_interface
        if issubclass(txtyp, TransportValuesType):
            show_type = TRANSPORT_VALUES_STORAGE_CLASS[txtyp.member_transport_type.storage_class]
        else:
            show_type = txtyp.storage_class
        return Map(name=txtyp.__name__, param_type=show_type)

    def convert(self, value, param: Optional[Parameter], context: Optional[Context]) -> Ti:
        # print("-- %s PARSE %r" % (self.name, value,))
        return self.field_info.parse_input(value, context)


class ParamNone(ParamInterface, TransportNone):
    pass


class ParamStr(ParamInterface, TransportStr):
    @classmethod
    def parse_arg(self, arg: str, _) -> str:
        return arg


class ParamIntStr(ParamInterface, TransportIntStr):
    pass


class ParamFloatStr(ParamInterface, TransportFloatStr):
    pass


class ParamInt(ParamInterface, TransportInt):
    @classmethod
    def parse_arg(self, arg: Union[str, int], _) -> int:
        if isinstance(arg, str):
            return int(arg)
        else:
            return arg


class ParamBool(ParamInterface, TransportBool):
    @classmethod
    def get_click_param_type(cls, info):
        return click.BOOL


class ParamEnum(ParamInterface, TransportEnum):
    @classmethod
    def parse_arg(cls, arg: Union[str, Any], context: Context) -> Any:
        name = arg if isinstance(arg, Enum) else str(arg).upper()
        return super().parse_arg(name, context)


class ParamTimestamp(ParamInterface, TransportTimestamp):
    pass

class ParamValues(ParamInterface, TransportValuesType[Ti, To]):
    @classmethod
    def parse_arg(cls, arg: Union[Sequence[str], Sequence[Ti]]) -> Sequence[Ti]:
        ## Click support - see the ParamType def, above
        if arg:
            mtyp: ParamInterface = cls.member_transport_type
            return tuple(map(mtyp.parse_arg, arg))
        else:
            return ()
class ParamAccountUnits(ParamInterface, AccountUnits):
    pass


class ParamInstrument(ParamInterface, InstrumentName):
    pass


class ParamFloat(ParamInterface, FloatValue):
    pass


class ParamPrice(ParamInterface, PriceValue):
    pass


class ParamLots(ParamInterface, LotsValue):
    pass


class ParamTradeId(ParamInterface, TradeId):
    pass


class ParamTransactionId(ParamInterface, TransactionId):
    pass


class ParamOrderId(ParamInterface, OrderId):
    pass


class ParamTime(ParamInterface, Time):
    pass


#
# Types Repository for Request Types
#

class ParamTypesRepository(TransportModelRepository):


    def init_enum_transport_type(self, etyp: type[Enum]) -> type[TransportEnumType]:
        base = super().init_enum_transport_type(etyp)
        name = "Param::" + base.__name__
        return new_class(name, (ParamEnum, base,))

    @classmethod
    def initialize_singleton(cls):
        s = cls()
        s.bind_types({
            bool: ParamBool,
            None.__class__: ParamNone,
            str: ParamStr,
            int: ParamInt,
            float: ParamFloatStr,
            double: ParamFloatStr,
            datetime: ParamTime,
            datetime64: ParamTime,
            Timestamp: ParamTime,
            InstrumentName: ParamInstrument,
            AccountUnits:  ParamAccountUnits,
            FloatValue: ParamFloat,
            PriceValue: ParamPrice,
            LotsValue: ParamLots,
            TradeId: ParamTradeId,
            TransactionId: ParamTransactionId,
            OrderId: ParamOrderId,
            Time: ParamTime
        })
        return s
