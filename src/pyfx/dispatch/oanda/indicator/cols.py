# data schemas [prototype]

import pandas as pd
import importlib_metadata as imd
from functools import partial
from immutables import Map
import inspect
import numpy as np
import numpy.typing as npt
import warnings

from pyfx.dispatch.oanda.fx_const import FxLabel
from pyfx.dispatch.oanda.indicator.common import get_annotation
from pyfx.dispatch.oanda.util.decorator import Decorator
from pyfx.dispatch.oanda.util.typeref import TypeRef
from pyfx.dispatch.oanda.models.get_instrument_candles200_response import CandlestickGranularity
from pyfx.dispatch.oanda.models.currency_pair import CurrencyPair

from pyfx.dispatch.oanda.indicator.price import PriceFilter

from abc import ABC, ABCMeta, abstractmethod
from collections.abc import Iterable, Mapping
from types import MemberDescriptorType
from typing import TYPE_CHECKING, Any, Callable, Generic, Literal, Optional, Union
from typing_extensions import (
    get_type_hints, get_origin, get_args,
    Protocol, Any, Self, ClassVar, TypeAlias, TypeVar
)


def get_dtype(annot) -> np.dtype:
    orig = get_origin(annot)
    if orig is np.ndarray:
        return get_dtype(get_args(annot)[1])
    elif isinstance(orig, type) and issubclass(orig, ArrayInterface):
        args = get_args(annot)
        if len(args) > 0:
            dt = args[0]
            if isinstance(dt, np.dtype):
                return dt
            else:
                return np.dtype(dt)
    try:
        return np.dtype(annot)
    except TypeError:
        warnings.warn("Unable to infer dtype from annotation %r. Usng np.dtype('O')" % (annot,),
                      stacklevel=2)
        return np.dtype("O")


#
# generalized types
#

T_dt = TypeVar("T_dt", bound=npt.DTypeLike)
T_data = TypeVar("T_data", bound=npt.ArrayLike)


class Named(Protocol):
    @property
    def __name__(self) -> str:
        raise NotImplementedError(self.__name__)


#
# column-oriented data model
#


T = TypeVar("T")


class BindableAttr(ABC, Generic[T]):
    # early prototype, a descriptor mixin class for MetaProperty (Descriptor mixin)

    if TYPE_CHECKING:
        __name__: str
        __scope__: type[T]

    @property
    def name(self) -> str:
        return self.__name__

    @property
    def scope(self) -> type[T]:
        return self.__scope__

    def __set_name__(self, scope: type[T], name: str):
        self.__name__ = name
        self.__scope__ = scope


class MetaProperty(property, BindableAttr, Decorator, Generic[T]):
    if TYPE_CHECKING:
        __name__: str

    @property
    def name(self) -> str:
        return self.__name__ if hasattr(self, "__name__") else "<Unnamed>"

    def __repr__(self) -> str:
        return "<%s %s at 0x%x>" % (self.__class__.__name__, self.name, id(self),)

    def __get__(self, obj: Optional[Self], objtype: Optional[type[Self]] = None) -> Union[MemberDescriptorType, T]:
        #
        # for purpose of __get__ this extends the original property implementation,
        # such that fget() will be called to access a value at the class scope,
        # when 'obj' is None
        #
        if obj is None:
            # access the property at class scope
            #
            # in some contexts, this may  return
            # a descriptor object
            value = self.fget(objtype, objtype)
        else:
            # access the property at instance scope
            value = self.fget(obj, objtype)
        if __debug__:
            #
            # During ABC class construction, this may need to return a descriptor at some points,
            # e.g for the "top class" of a metaproperty structure, such as when an underlying
            # attribute value is being initialized in the containing class while accessed through
            # a metaproperty definition for that class
            #
            # Example: __columns__ and __indices__ (slots) in DataSchema, accessed
            # respectively via the 'columns' and 'indices' metaproperties. The class
            # of DataSchema would not define any __columns__ or __indices__ values
            # but would define each as a member descriptor, insofar as under __slots__
            #
            # ... as such:
            #
            # This test will generally be avoided when called at the class scope,
            # for a class having ABC in its immediate base class tuple
            #
            # The test will be avoided entirely under e.g 'python -O'
            #
            # During normal python debugging, the test would be reached for:
            # (A) a metaproperty accessed at the instance scope, and for
            # (B) a metaproperty accessed at the class scope for some class not defined
            #     with ABC in the class' direct base classes
            #
            if not (obj is None and ABC in objtype.__bases__) and inspect.isdatadescriptor(value):
                #
                # assuming that any value accessed under a @metaproperty would not
                # be bound to a descriptor object under normal application, this may
                # represent - through some indirection - an "unbound descriptor" state
                #
                raise AssertionError("Unbound data descriptor", value, self, obj, objtype)
        return value

def metaproperty(decorated: Callable):
    return MetaProperty.decorate_new(decorated)


class Interface(ABC):

    @classmethod
    def attrs_by_type(cls, acls: type):
        # utility method
        dct = vars(cls)
        return {name: attr for name, attr in dct.items() if isinstance(attr, acls)}


class InterfaceType(Interface, ABCMeta, type):
    pass


T_default = TypeVar("T_default")

T_view = TypeVar("T_view", bound="ArrayView")


class ArraySchema(Generic[T, T_view], ABC):
    __slots__ = "__members__", "__names__", "__scope__"

    if TYPE_CHECKING:
        __names__: tuple[str]
        __members__: Map[str, T]
        __scope__: Optional[Named]

    @property
    def names(self) -> tuple[str]:
        return self.__names__

    @property
    def members(self) -> Map[str, T_view]:
        return self.__members__

    @property
    def scope(self) -> Optional[Named]:
        return self.__scope__

    def __init__(self, members: Optional[Union[Mapping[str, T_view], Iterable[tuple[str, T_view]]]] = None,
                 scope: Optional[Named] = None):
        if members is not None:
            mdct = members if isinstance(members, dict) else dict(members)
            self.__names__ = tuple(mdct.keys())
            self.__members__ = Map(mdct)
        self.__scope__ = scope

    def __getitem__(self, name: str) -> T:
        return self.__members__[name]

    def get(self, name: str, default: T_default) -> Union[T, T_default]:
        return self.__members__.get(name, default)

    def __iter__(self):
        return self.__members__.__iter__()

    def __len__(self) -> int:
        return len(self.__members__)

    def __repr__(self) -> str:
        scope = self.__scope__ if hasattr(self, "__scope__") else None
        sname = "<Unscoped>" if scope is None else scope.__name__
        if hasattr(self, "__names__"):
            mstr = ", ".join(self.__names__)
        else:
            mstr = ""
        return "<%s %s [%s] at 0x%x>" % (self.__class__.__name__, sname, mstr, id(self),)


class ColumnSchema(ArraySchema[T, T_view]):
    pass


class IndexSchema(ArraySchema[T, T_view]):
    pass


class DataModelInterface(Interface, metaclass=InterfaceType):

    @metaproperty
    @abstractmethod
    def columns(cls: type[Self], self: Union[Self, None]) -> ColumnSchema:
        raise NotImplementedError(vars(cls).get("columns", "columns"))  # ...

    @metaproperty
    @abstractmethod
    def indices(cls: type[Self], self: Union[Self, None]) -> IndexSchema:
        raise NotImplementedError(vars(cls).get("indices", "indices"))


class DataSchema(DataModelInterface, ABC):

    __slots__ = "__columns__", "__indices__"

    if TYPE_CHECKING:
        __columns__: ClassVar[ColumnSchema["ArrayView", "ArrayModel"]]
        __indices__: ClassVar[IndexSchema["IndexView", "IndexModel"]]

    @metaproperty
    ## FIXME duplicate methods in this initial prototype
    ##
    ## the primary way to test which one is being called is through a backtrace ...
    ##
    def columns(scope: Union[Self, type[Self]], base: type[Self]) -> ColumnSchema["ArrayView", "ArrayModel"]:
        # if 'scope' is 'base' then this is being accessed at class scope
        return scope.__columns__

    @metaproperty
    def indices(scope: Union[Self, type[Self]], base: type[Self]) -> IndexSchema["IndexView", "IndexModel"]:
        # if 'scope' is 'base' then this is being accessed at class scope
        return scope.__indices__

    def __init_subclass__(cls) -> None:
        annot = get_type_hints(cls)
        cols = None if hasattr(cls, "__columns__") and isinstance(cls.__columns__, Iterable) else dict()
        inds = None if hasattr(cls, "__indices__") and isinstance(cls.__indices__, Iterable) else dict()
        for name, attr in cls.__dict__.items():
            if isinstance(attr, ArrayModel):
                if not hasattr(attr, "__dtype__"):
                    field_annot = annot.get(name, None)
                    if not hasattr(attr, "__name__"):
                        attr.__name__ = name
                    if field_annot is not None:
                        dtype = np.dtype(field_annot)
                        attr.__dtype__ = dtype
                if isinstance(attr, ColumnDesc) and cols is not None:
                    cols[name] = attr
                if isinstance(attr, IndexDesc) and inds is not None:
                    inds[name] = attr
        if cols is not None:
            cls.__columns__ = ColumnSchema(cols, cls)
        if inds is not None:
            cls.__indices__ = IndexSchema(inds, cls)


class DataProvider(metaclass=InterfaceType):
    # FIXME :unused prototype
    __slots__ = "__name__",

    if TYPE_CHECKING:
        __name__: str

    @metaproperty
    def name(cls: type[Self], obj: Union[Self, None]):
        if obj is None:
            return cls.__name__
        else:
            return obj.__name__


class PyDataProvider(DataProvider):
    # FIXME :unused prototype
    #
    # application / metadata support TBD
    #
    __slots__ = "__distribution__", "__version__"

    if TYPE_CHECKING:
        __distribution__: Optional[imd.Distribution]

    @property
    def distribution(self):
        try:
            return self.__distribution__
        except AttributeError:
            name = self.name
            try:
                dist = imd.distribution(name)
            except ImportError:
                dist = None
            self.__distribution__ = dist
            return dist

    @property
    def version(self):
        try:
            return self.__version__
        except AttributeError:
            dist = self.distribution
            if dist is None:
                version = None
            else:
                version = dist.version
            self.__version__ = version
            return version

#
# Generic reference API
#


class ArrayInterface(Generic[T_dt]):
    __slots__ = "__weakref__", "__name__", "__iname__", "__scope__", "__atype__", "__dtype__"

    if TYPE_CHECKING:
        __name__: str
        __iname__: str
        __scope__: DataModelInterface
        __dtype__: T_dt
        __atype__: TypeRef

    @property
    def name(self) -> str:
        return self.__name__

    @property
    def scope(self) -> DataModelInterface:
        return self.__scope__

    @property
    def dtype(self) -> T_dt:
        return self.__dtype__

    @property
    def atype(self) -> Optional[TypeRef]:
        try:
            return self.__atype__
        except AttributeError:
            return None

    def __set_name__(self, scope: type[T], name: str):
        # this method may be overidden in a subclass
        self.__name__ = name
        self.__iname__ = name
        self.__scope__ = scope
        hints = get_type_hints(scope)

        atyp = get_annotation(name, scope)

        if atyp is not None:
            if not hasattr(self, "__type__"):
                self.__atype__ = atyp
            if not hasattr(self, "__dtype__") and isinstance(scope, type):
                self.__dtype__ = get_dtype(atyp)

    def __init__(self, name: str, dtype: Optional[T_dt] = None):
        self.__name__ = name
        if dtype is not None:
            self.__dtype__ = dtype

    def __repr__(self) -> str:
        attr_p = partial(hasattr, self)
        name = self.__name__ if attr_p("__name__") else "<Anonymous>"
        dt = self.__dtype__ if attr_p("__dtype__") else "<Untyped>"
        return "<%s %s (%s) at 0x%x>" % (self.__class__.__name__, name, dt, id(self))


class ArrayModel(ArrayInterface[T_dt]):
    pass


class ArrayView(ArrayInterface[T_dt]):
    pass


class Array(ArrayInterface[T_dt], Generic[T_dt, T_data], ABC):
    __slots__ = "__schema__", "__idx__", "__data__"

    if TYPE_CHECKING:
        __schema__: ArrayModel[T_dt]
        __idx__: int
        # the __data__ value is accessed generally via __get__,
        # internally via initial deref()
        __data__: T_data

    def __init__(self, name: str, data: Optional[T_data] = None):
        self.__name__ = name
        if data is not None:
            self.__data__ = data

    @property
    def dtype(self) -> T_dt:
        # accessed e.g under deref(), should be initialized during schema/model/view init
        return self.schema.dtype

    @property
    def schema(self) -> ArrayModel[T_dt]:
        # original concept: schema for an array data object
        #
        # accessed for e.g a DfColumn attr of FxQuotesView under tests
        ##
        # print("-- SCHEMA 02 %r => %r" % (self, self.__schema__))
        return self.__schema__  # not a DataSchema here. ColumnModel e.g

    @property
    def index(self) -> int:
        return self.__idx__

    @property
    @abstractmethod
    def shape(self) -> tuple[int, ...]:
        #
        # real array shape
        #
        raise NotImplementedError(self.shape)


#
# Generic API for column and index referencing
#


class DataDesc(ArrayInterface[T_dt]):
    # mixn class representing a direct interface onto a concrete data object.
    #
    # Usage:
    # - Column, ColumnView
    # - Index, IndexView

    # iname here:
    # intemediate (interface) name for this column/view or index/view
    # - closed within the containing object's data schema
    # - may differ per provider, juxtaposed to the generalized "schema name" for a column
    # - e.g iname "o" for the generalized quotes "open" column, in an implementation onto an FxTrade API

    @property
    def iname(self):
        # implementation name: generalization for a concrete column name or index name
        return self.__iname__

    def __init__(self, iname: str):
        ## set the implementation name from a value provided to the constructor
        self.__iname__ = iname

    def __set_name__(self, scope: type[T], name: str):
        ## set the generalized object name from the attribute name
        self.__name__ = name
        self.__scope__ = scope

        if not hasattr(self, "__dtype__") and isinstance(scope, type):
            annot = get_annotation(name, scope)
            if annot is not None:
                self.__dtype__ = get_dtype(annot)

    @abstractmethod
    def deref(self, obj: DataSchema):
        raise NotImplementedError(self.deref)

    def __get__(self, obj: Optional[DataSchema], objtype: Optional[type[DataSchema]] = None) -> Union[T_data, int]:

        if obj is None:
            return self
        try:
            return self.__data__
        except AttributeError:
            data = self.deref(obj)
            self .__data__ = data
            return data


#
# -- index generalization
#


class IndexDesc(ArrayInterface[T_dt]):
    pass


class TimeIndexDesc(IndexDesc[T_dt]):
    pass


class IndexModel(IndexDesc, ArrayModel[T_dt]):
    pass


class TimeIndexModel(TimeIndexDesc, IndexModel[T_dt]):
    pass


class IndexView(IndexDesc[T_dt], DataDesc[T_dt], ArrayView[T_dt]):
    def __init__(self, name: str):
        self.__name__ = name


class TimeIndexView(TimeIndexDesc, IndexView[T_dt]):
    pass


class Index(IndexDesc[T_dt], DataDesc[T_dt], Array[T_dt, T_data]):
    __slots__ = "__schema__",

    if TYPE_CHECKING:
        __schema__: IndexModel[T_dt]

    def __set_name__(self, scope: type[T], name: str):
        # generally similar to Column.__set_name__()
        super(DataDesc, self).__set_name__(scope, name)

        sch: DataSchema = scope.schema
        sidx = sch.indices.members.get(name)
        if sidx is not None:
            self.__schema__ = sidx


class TimeIndex(TimeIndexDesc, Index[T_dt, T_data]):
    pass


#
# -- column generalization
#


class ColumnDesc(ArrayInterface[T_dt]):
    pass


class ColumnModel(ColumnDesc[T_dt], ArrayModel[T_dt]):
    ## e.g schema model for a column
    pass


class ColumnView(ColumnDesc[T_dt], DataDesc[T_dt], ArrayView[T_dt]):
    ## e.g provider view for a column defined in some explicit (generalzied) or implicit (provider-local) schema
    pass


class ArrayBinding(Array[T_dt, T_data]):
    pass


class Column(ColumnDesc[T_dt], DataDesc[T_dt], Array[T_dt, T_data]):
    ## e.g column interface onto some object storing an actual data object

    @property
    def offset(self) -> int:
        return self.__idx__

    def __set_name__(self, scope: type[T], name: str):
        # generally similar to Index.__set_name__()
        super(DataDesc, self).__set_name__(scope, name)

        sch: DataSchema = scope.schema
        # this accessor differs to an Index data desc:
        scol = sch.columns.members.get(name)
        if scol is not None:
            self.__schema__ = scol


class DfValues(Array[T_dt, T_data]):

    def shape(self, obj: DataSchema):
        try:
            data = self.__data__
        except AttributeError:
            data = self.deref(obj)
            self.__data__ = data
        return data.shape()


class DfColumn(Column[T_dt, T_data], DfValues[T_dt, T_data]):

    def index_for(self, obj: "DataView[T_data]"):
        try:
            return self.__idx__
        except AttributeError:
            cols: Mapping[str, int] = obj.columns
            # print("... COLS %r" % cols)
            idx = cols[self.__iname__]
            self.__idx__ = idx
            return idx

    def deref(self, obj: DataSchema):
        #
        # memoization for this value is handled mainly under DataDesc.__get__(...)
        #
        idx = self.index_for(obj)
        data: np.ndarray = obj.data.iloc[:, idx].to_numpy(copy=False)
        dt = self.dtype
        if data.dtype == dt:
            return data
        else:
            return data.astype(dt, copy=False)


class DfColumnGroup(DfColumn):
    slots = "__contiguous__", "__mincol__", "__maxcol__"

    if TYPE_CHECKING:
        # reusing the __iname__ slot, here as a tuple of concrete column names
        __iname__: tuple[str, ...]
        iname: tuple[str, ...]
        __continguous__: bool
        __mincol__: int
        __maxcol__: int

    @property
    def dtype(self):
        return self.__dtype__

    def __init__(self, *names: tuple[str, ...]):
        self.__iname__ = names

    def __set_name__(self, scope: type[T], name: str):
        # ensure the correct __set_name__() call is used here,
        # to not ovewrite __iname__ as set in the descriptor's ctor
        super(Column, self).__set_name__(scope, name)

    def contiguous(self, obj: "DataView[T_data]"):
        data: pd.DataFrame = obj.data
        cols = tuple(data.columns)
        imap = {name: cols.index(name) for name in self.iname}
        indices = np.array(tuple(sorted(imap.values())))
        imin = indices.min()
        imax = indices.max() + 1
        contiguous = True
        for n in np.arange(imin, imax):
            if n not in indices:
                contiguous = False
                break
        self.__mincol__ = imin
        self.__maxcol__ = imax
        self.__continguous__ = contiguous
        return contiguous

    def deref(self, obj: "DataView[T_data]"):
        data = obj.data
        if self.contiguous(obj):
            pdata = data.iloc[:, self.__mincol__:self.__maxcol__]
        else:
            pdata = data.loc[:, self.iname]
        return pdata.to_numpy(self.dtype.type, copy=False)


class DfIndex(Index[T_dt, T_data], DfValues[T_dt, T_data]):
    def deref(self, obj: "DataView[T_data]"):
        #
        # memoization for this object is handled mainly under DataDesc.__get__(...)
        #
        pidx: pd.Index = obj.data.index
        dt: np.dtype = self.dtype
        return pidx.to_numpy(dt, copy=False)


class TimeIndexView(IndexView[T_dt]):
    pass


class TimeIndex(Index[T_dt, T_data]):
    pass


class DfTimeIndex(TimeIndex, DfIndex):
    pass


class DfUSecIndex(DfTimeIndex, DfIndex):
    # usage e.g: time coordinates for charting applications
    pass


class DataSchemaType(DataModelInterface, InterfaceType, metaclass=InterfaceType):
    if TYPE_CHECKING:
        __schema__: ClassVar[type[DataSchema]]

        __columns__: ClassVar[type[ArrayModel]]
        __indices__: ClassVar[type[IndexModel]]

    def __new__(mcls: type[Self], name: str, bases: tuple[type, ...], ns: dict[str, Any]) -> Self:
        new_cls: Self = super().__new__(mcls, name, bases, ns)

        attr_p = partial(hasattr, new_cls)
        if attr_p("__schema__"):
            # inherit columns, indices from the new class' model (schema) to new_cls
            m = new_cls.__schema__
            m_attr_p = partial(hasattr, m)
            if m_attr_p("__columns__") and not attr_p("__columns__"):
                new_cls.__columns__ = m.__columns__
            if m_attr_p("__indices__") and not attr_p("__indices__"):
                new_cls.__indices____ = m.__indices__

        return new_cls

    @metaproperty
    def schema(scope: Union[Self, type[Self]], base: type[Self]) -> DataSchema:
        # print("-- M SCHEMA %r %r => %r" % (scope, base, scope.__schema__,))
        return scope.__schema__
        # if self is None:
        #     return cls.__schema__
        # else:
        #     return self.__schema__

    @metaproperty
    def columns(scope: Union[Self, type[Self]], base: type[Self]) -> Iterable[ColumnModel]:
        return scope.schema.columns

    @metaproperty
    def indices(scope: Union[Self, type[Self]], base: type[Self]) -> Iterable[IndexModel]:
        return scope.schema.indices

#
# preliminary provider model
#


T_model = TypeVar("T_model", bound=DataSchema)  # TBD no generic args here


class ProviderModel(DataSchema):
    if TYPE_CHECKING:
        __provider__: "ProviderView"

    @metaproperty
    def provider(scope: Union[Self, type[Self]], base: type[Self]):
        return scope.__provider__

    def __init__(self, provider: "ProviderView",
                 cols: Optional[ColumnSchema] = None,
                 indices: Optional[IndexSchema] = None
                 ):
        super()
        self.__provider__ = provider
        if cols is not None:
            self.__columns__ = cols
        if indices is not None:
            self.__indices__ = indices


class ProviderView(DataSchemaType, Generic[T_model], metaclass=DataSchemaType):
    if TYPE_CHECKING:
        __schema__: type[T_model]
        __model__: ProviderModel

    @metaproperty
    def model(scope: Union[Self, type[Self]], base: type[Self]) -> ProviderModel:
        return scope.__model__

    @metaproperty
    def columns(scope: Union[Self, type[Self]], base: type[Self]):
        # provider column j/t schema columns
        return scope.model.columns

    @metaproperty
    def indices(scope: Union[Self, type[Self]], base: type[Self]):
        # provider indices (?) j/t schema indices
        return scope.model.indices

    def __new__(mcls: type[Self], name: str, bases: tuple[type, ...], ns: dict[str, Any]) -> Self:
        new_cls: Self = super().__new__(mcls, name, bases, ns)

        mcols: Map[str, ColumnView] = Map(new_cls.attrs_by_type(ColumnView))
        scols = new_cls.schema.columns
        for name, col in mcols.items():
            schcol = scols.get(name, None)
            if name is None:
                continue
            if not hasattr(col, "__dtype__") and hasattr(schcol, "__dtype__"):
                # inherit provider column dtype from the schema column
                col.__dtype__ = schcol.__dtype__
            # print("-- CSCH %r %r" % (col, scols[name],))
            col.__schema__ = schcol
        mindices: Map[str, IndexView] = Map(new_cls.attrs_by_type(IndexView))
        new_cls.__model__ = ProviderModel(new_cls, mcols, mindices)

        return new_cls


#
# model view types
#


class DataView(Generic[T_data], ABC, metaclass=DataSchemaType):
    ## Usage:
    # - NDView
    # - DataframeView
    #   - QuotesView
    #     - FxComponentView

    __slots__ = "__data__", "__provider__", "__columns__", "__indices__"

    if TYPE_CHECKING:
        __data___: T_data
        __provider__: ProviderView[T]
        __columns__: Mapping[str, int]
        __indices__: Mapping[str, str]
        columns: Mapping[str, int]

    @property
    def data(self) -> T_data:
        return self.__data__

    @metaproperty
    def provider(scope: Union[Self, type[Self]], base: type[Self]) -> ProviderView[T]:
        # Implementation Note
        #
        # If `scope` is `base`, this is being accessed at class scope
        #
        return scope.__provider__

    def __init__(self, data: Optional[T] = None):
        if data is not None:
            self.__data__ = data


#
# specialization for specific data formats
#

class DataframeView(DataView[pd.DataFrame], metaclass=DataSchemaType):

    @metaproperty
    def columns(scope: Union[Self, type[Self]], base: type[Self]):
        return scope.__columns__

    @metaproperty
    def indices(scope: Union[Self, type[Self]], base: type[Self]):
        return scope.__indices__

    def __init__(self, data: pd.DataFrame):
        self.__data__ = data
        provider = self.provider
        cols = tuple(data.columns)
        # provider[open] -> 'o' would be the column name for schema[open]

        self.__columns__ = Map((k, cols.index(v.iname),) for k, v in provider.columns.items())
        self.__indices__ = Map((k, v.name,) for k, v in provider.indices.items())


#
# initial testing
#


class QuotesSchema(DataSchema):
    # FX Quotes Schema
    open: ColumnModel[float] = ColumnModel[np.double]("Open")
    high:  ColumnModel[float] = ColumnModel[np.double]("High")
    low: ColumnModel[float] = ColumnModel[np.double]("Low")
    close: ColumnModel[float] = ColumnModel[np.double]("Close")
    volume: ColumnModel[int] = ColumnModel[np.uint32]("Volume")
    time: TimeIndexModel[pd.Timestamp] = TimeIndexModel[pd.Timestamp]("Time")
    ##
    # frequency may be set within some application context,
    # can potentially be inferred from a set of continguous
    # time values
    ##
    # period = FrequencyIndexView("period")
    # usec = TimestampIndexView("usec")
    #
    ##
    # could be inherited down to the 'view' level,
    # but this would be missed by static type checking
    ##
    frequency: Union[str, pd.PeriodDtype]  # see infer_freq
    symbol: CurrencyPair
    # provider: ...


class QuotesSchemaCls(DataSchemaType):
    __schema__: ClassVar[type[QuotesSchema]] = QuotesSchema


class QuotesView(DataframeView,  metaclass=QuotesSchemaCls):
    pass


class QuotesProviderCls(ProviderView, QuotesSchemaCls):
    pass


FxComponentName: TypeAlias = Union[Literal["ask"], Literal["bid"], Literal["mid"]]

#
# adding QuotesSchemaCls to the base class list for FxComponent,
# this allows for using FxComponent as a metaclass for FxComponentView
#


class FxComponent(ProviderView[QuotesSchema], QuotesSchemaCls, metaclass=QuotesProviderCls):
    #
    # comopnent data view, i.e within some component
    # of FxTrade quotes series (ask, bid, mid)
    #

    __component__: FxComponentName  # = ProviderField()
    # ^ default component for quotes requests in the FxTrade v20 REST API: "mid"

    # provider = FxPyProvider ...

    ## the cls' actual data model:
    open: ColumnView[np.double] = ColumnView(FxLabel.OPEN.value)
    high: ColumnView[np.double] = ColumnView(FxLabel.HIGH.value)
    low: ColumnView[np.double] = ColumnView(FxLabel.LOW.value)
    close: ColumnView[np.double] = ColumnView(FxLabel.CLOSE.value)
    volume: ColumnView[np.dtype(int)] = ColumnView(FxLabel.VOLUME.value)
    time: TimeIndexView[pd.Timestamp] = TimeIndexView(FxLabel.TIME.value)  # named index view

    # quotes: AggregateModel[4, np.double] = AggregateView("o", "h", "l", "c")


class FxComponentFrame(QuotesView, metaclass=FxComponent):
    # FxComponent View onto a dataframe

    __provider__: ClassVar[type[ProviderView]] = FxComponent
    __component__: FxComponentName

    @metaproperty
    def component(obj: Self, scope: type[Self]):
        return obj.__component__

    @property
    def granularity(self) -> CandlestickGranularity:
        # TBD see infer_freq()
        # albeit absent of any frequency -> granularity mapping at this time
        return self.data.attrs['granularity']

    @property
    def frequency(self) -> str:
        return self.data.attrs["freq"]  # TBD

    @property
    def instrument(self) -> str:
        return self.data.attrs["instrument"]

    def resample(self, freq: str):
        return NotImplemented

    # component: FxComponentName # = ProviderField()

    # the cls' actual data model
    #
    # TBD: inherit data column naming from the provider model.
    # This reuses other constants
    #
    open: npt.NDArray[np.double] = DfColumn(FxLabel.OPEN.value)
    high: npt.NDArray[np.double] = DfColumn(FxLabel.HIGH.value)
    low: npt.NDArray[np.double] = DfColumn(FxLabel.LOW.value)
    close: npt.NDArray[np.double] = DfColumn(FxLabel.CLOSE.value)
    volume: npt.NDArray[np.dtype(int)] = DfColumn(FxLabel.VOLUME.value)
    # time: named index
    time: pd.DatetimeIndex = DfTimeIndex(FxLabel.TIME.value)

    ## aggregate column
    quotes: npt.NDArray[np.double] = DfColumnGroup("o", "h", "l", "c")


class FxFrame(DataView[T_data]):
    __slots__ = "__ask__", "__bid__", "__mid__"

    if TYPE_CHECKING:
        volume: npt.NDArray[np.dtype(int)]
        time: FxComponentFrame.time

    # TBD binding additional indicators
    #
    # TBD consistent metadata mapping

    instrument = FxComponentFrame.instrument

    @property
    def ask(self) -> pd.DataFrame:
        try:
            return self.__ask__
        except AttributeError:
            ask = self.data[FxLabel.ASK.value]
            self.__ask__ = ask
            return ask

    @property
    def bid(self) -> pd.DataFrame:
        try:
            return self.__bid__
        except AttributeError:
            bid = self.data[FxLabel.BID.value]
            self.__bid__ = bid
            return bid

    @property
    def mid(self) -> pd.DataFrame:
        try:
            return self.__mid__
        except AttributeError:
            #
            # this would raise another AttributeError, if one or both
            # of __ask__ and __bid__ has not been set
            #
            ask = self.ask
            bid = self.bid
            mid: pd.DataFrame = (ask + bid) / np.short(2.0)
            self.__mid__ = mid
            mid_name = FxLabel.MID.value
            mid.name = mid_name

            #
            # memoize the mid quotes in the dataframe, for purpose of storage/retrieval
            #
            # the values will not be rounded or truncated to instrument precision here
            #
            data = self.data
            for colname in mid.columns:
                data.loc[:, (mid_name, *colname,)] = mid[colname]

            self.__mid__ = mid
            return mid


if __name__ == "__main__":

    # TBD: event-oriented descriptors
    # - e.g set data, update (append or prepend) data, clear data
    # - chaining for callbacks, indicators from set or update
    # - concurrent calculation under a thread pool
    #
    # Note: FxComponentView.open returns the actual descriptor object initialized to that attribute, in the class
    #

    from pyfx.dispatch.oanda.kernel.fxcmds import load_quotes
    import pandas as pd

    df: pd.DataFrame = load_quotes("~/wk/python_wk/pyfx_wk/pyfx_dispatch_oanda/examples/quotes.npz")

    # thunk = test_yf()

    test_df = pd.concat([df.loc[:, 'ask'], df.loc[:, "volume"]], axis=1, copy=False)

    qv = FxComponentFrame(test_df)
    qv.__component__ = "ask"

    print("Open : %r" % qv.open)

    qdf = FxFrame(df)
    print("Mid: %r" % qdf.mid)

    #
    # needs application (provider) integration for truncating values to instrument precision
    #
    tpf = PriceFilter("price")
    typical_price = tpf.apply(qdf.mid)
    print("Typical price [mid]: %r" % typical_price)

    from pyfx.dispatch.oanda.app.fx import TradeProfile

    def iround(profile: TradeProfile, frame: FxFrame):
        with profile.instrument(frame.attrs['instrument']) as inst:
            p = inst.display_precision
            # tfact = 10**p
            # return (np.round(frame, p), np.trunc(frame * tfact) / tfact)
            return np.round(frame, p)

    ## tests
    # %timeit qv.open
    # > 70.8 ns ± 13.8 ns per loop (mean ± std. dev. of 7 runs, 10,000,000 loops each)
    # ^ reuses the value from the initial dereference
    #
    # df = qv.data
    # %timeit df.o
    # > 2.67 µs ± 580 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)
    # ^ similar ? but notably slower ...
    #
    # df.columns
    # => Index(['o', 'h', 'l', 'c', 'volume'], dtype='object')
    #
    # %timeit df.iloc[:, 0]
    # > 21.4 µs ± 1.57 µs per loop (mean ± std. dev. of 7 runs, 100,000 loops each)
    #
    # !!
    # df.iloc[:, 0] is df.o
    # => False
    #
    # !!
    # df.iloc[:, 0] is df.iloc[:, 0]
    # => False
    #
    # df.o is df.o
    # => True
    #
    # getattr(df, "o") is getattr(df, "o")
    # => True

    # add'l test:
    #
    # open = qv.__class__.open.deref(qv)
    # first = open[0]
    # qv.__class__.open.deref(qv)[0] is first
    # => False # there is a data copy being produced here

    # not unimpressive, even with data copying:
    # In [40]: %timeit qv.__class__.open.deref(qv)[0]
    # ...

    # ...
    # qv.__class__.open.dtype # ?

    # qv.columns # columns for the view
    # qv.__class__.columns # model columns
    # QuotesModel.columns # same object as qv.__class__.columns
    #
    # qv.schema
