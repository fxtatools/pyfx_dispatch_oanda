"""Common classes for trade-dependent order details

This module defines a small number of mixin classes, primiarily
classes used in field values of a SetTradeDependentOrdersRequest,
applicable in calls to `DefaultApi.set_trade_dependent_orders()`

This module also defines a custom TransportType to provide protocol
support for parsing and representation of state values with this set
of classes.

**Trade-Dependent State**

When constructing a SetTradeDependentOrdersRequest, the following
fields in the request object may be set to `None` or to an instance
of the corresponding TradeDependentClass:
- `take_profit` as `TakeProfitDetails` or `None`
- `stop_loss` as `StopLossDetails` or `None`
- `trailing_stop_loss` as `TrailingStopLossDetails` or `None`
- `guaranteed_stop_loss` as `GuaranteedStopLossDetails` or `None`

In effect, these represent nullable fields.

For these fields of a SetTradeDependentOrdersRequest object, the
value `None` will have a specific meaning, distinct to the
significance of the field's absence within the request.

- Within the request object, the absence of the field would indicate
  that "No action" is requested.

- The presence of the value `None` in the respective field would
  indicate that the request is for cancelling an order of the
  corresponding order type, when such an order exists that would
  be matched by the order request.

- As a third possible state for each field, an instanace of the
  corresponding TradeDependentDetails class may be provided for
  that field. The type of the object would be dependent on
  the exact syntax of the field. In the general case, this object
  would provide a request for activation of a trade-dependent
  order of a type correpsonding to the respective request field.

**Trade-Dependent Classes**

The following fields are supported in all trade-dependent
classes:

- stop `distance` for *price-relative activation* of a
  trade-dependent order

- stop `price` for *price-specific activation* of a
  trade-dependent order, where supported for the type
  of the order request

- `time_in_force` for the trade-dependent order, by default
  `GTC` i.e "Good until cancelled"

- `gtd_time` for the trade-dependent order. A value may be
   provided for this field, when `time_in_force`is provided
   as `GTD`

An aditional field is supported in the v20 API,
`client_extensions`. This field should generally not be set
for orders in accounts used with the MetaTrader4 terminal.

**Price-Specific and Price-Relative Activation**

For specifying a price-specific order activation, the stop
`price` field may be provided with a value, in the following
classes:
- `StopLossDetails` (trade-dependent stop loss orders)
- `TakeProfitDetails` (trade-dependent take profit orders)
- `GuaranteedStopLossDetails` (trade-dependent guaranteed
   stop loss orders)

For these types of order, a value must be provided for exactly
one of the of `price` or `distance` fields.

For all trade-dependent classes, when the `distance` field is
provided, it specifies a price-relative form of activation
for the order. This value would be provided in price units.

Trailing Stop orders support only the price-relative form of
activation, i.e `distance` in price units.

**See also**

- `DefaultApi.set_trade_dependent_orders()`
- `SetTradeDependentOrdersRequest`
"""

from abc import ABC
from collections.abc import Mapping
from types import new_class
from typing import Annotated, Any, Literal, Optional, Union
from typing_extensions import ClassVar, TypeAlias, TypeVar

from ..util.naming import exporting

from ..transport.data import ApiObject, ApiClass, ModelState, TransportObjectType
from ..transport.transport_fields import TransportField
from ..transport.transport_base import TransportType, TransportNone
from ..transport.transport_common import IntermediateObject
from .client_extensions import ClientExtensions
from .common_types import PriceValue, Time
from .time_in_force import TimeInForce


class TradeDependentClass(ApiClass):
    """Metaclass supoprt for nullable TradeDependentDetails classes"""

    def __instancecheck__(self, instance: Any) -> bool:
        if instance is None:
            return True
        else:
            return super().__instancecheck__(instance)


class TradeDependentDetails(ApiObject, ABC, metaclass=TradeDependentClass):
    """Mixin class for trade-dependent order details"""

    distance: Annotated[Optional[PriceValue], TransportField(None)]
    """Specifies the distance (in price units) from the Trade's open price
    to use in activting the trade-dependent Order.

    For trade-dependent orders providing a price parameter, only one of the
    distance and price parameters may be specified.
    """

    time_in_force: Annotated[TimeInForce, TransportField(None, alias="timeInForce")] = TimeInForce.GTC  # type: ignore
    """The time in force for the created trade-dependent Order.

    This may only be GTC, GTD or GFD.
    """

    gtd_time: Annotated[Optional[Time], TransportField(None, alias="gtdTime")]
    """The date when the trade-dependent Order will be cancelled if `time_in_force` is `GTD`.
    """

    client_extensions: Annotated[Optional[ClientExtensions], TransportField(None, alias="clientExtensions")]
    """The Client Extensions to add to the trade-dependent Order when created.
    """


    @classmethod
    def ensure_transport_type(cls) -> Optional[TransportType]:
        if ABC in cls.__bases__:
            return
        if hasattr(cls, "transport_type"):
            return cls.transport_type
        elif hasattr(cls, "types_repository"):
            repository = cls.types_repository
            rtyp = repository.find_transport_type(cls)
            if rtyp:
                cls.transport_type = rtyp
                return rtyp
            else:
                name = "Transport" + cls.__name__ + "Type"

                def init_ns(namespace: dict):
                    namespace["serialization_type"] = TransportTradeDependent.serialization_type
                    namespace["serialization_class"] = TransportTradeDependent.serialization_class
                    namespace["storage_type"] = cls
                    namespace["storage_class"] = cls

                txcls = new_class(name, (TransportTradeDependent,), None, init_ns)
                repository.bind_transport_type(cls, txcls)
                cls.transport_type = txcls
                return txcls
        else:
            raise RuntimeError("Unable to infer transport type", cls)


TradeDependentObject: TypeAlias = Union[TradeDependentDetails, Literal[None]]
TradeDependentIntermediate: TypeAlias = Union[Mapping[str, Any], Literal[None]]

T_trade = TypeVar("T_trade", bound=TradeDependentObject)


class TransportTradeDependent(TransportObjectType[T_trade, TradeDependentIntermediate], ABC):
    """Transport type for nullable trade-dependent transaction values"""

    serialization_type: ClassVar[type] = TradeDependentObject
    serialization_class: ClassVar[type] = object

    @classmethod
    def parse(cls, unparsed: Union[T_trade, IntermediateObject]) -> T_trade:
        if unparsed:
            return super().parse(unparsed)
        else:
            return None

    @classmethod
    def unparse_py(cls, value: T_trade) -> IntermediateObject:
        if value is None:
            return None
        else:
            return super().unparse_py(value)

    @classmethod
    def unparse_bytes(cls, value: T_trade) -> bytes:
        if value is None:
            return TransportNone.unparse_bytes(value)
        else:
            return super().unparse_bytes(value)

    @classmethod
    def unparse_url_bytes(cls, value: T_trade) -> bytes:
        ## not supported: unparse an ApiObject to a URL-encoded value (Swagger/OpenAPI 2)
        raise NotImplementedError(cls.unparse_url_bytes)

    @classmethod
    def unparse_url_str(cls, value: T_trade) -> bytes:
        ## not supported: unparse an ApiObject to a URL-encoded value (Swagger/OpenAPI 2)
        raise NotImplementedError(cls.unparse_url_str)

    @classmethod
    def get_state(cls, object):
        if object:
            return super().get_state(object)

    @classmethod
    def restore_state(cls, field, m_object, state: ModelState):
        if state:
            super().restore_state(field, m_object, state)
        else:
            cls.__dict__[field] = None

    @classmethod
    def restore_member_state(cls, field, m_object, m_value: Optional[ModelState[T_trade]]) -> Optional[ModelState[T_trade]]:
        if m_value:
            return super().restore_member_state(field, m_object, m_value)
        else:
            return None


    @classmethod
    def get_display_string(cls, value: T_trade) -> str:
        raise NotImplementedError(cls.get_display_string)


class TradeDependentPriceDetails(TradeDependentDetails, ABC):
    """Mixin class for trade-dependent order details that may be actuated on a stop price
    """

    price: Annotated[Optional[PriceValue], TransportField(None)]
    """The price that the Order will be triggered at.

    Only one of the price and distance fields may be specified.
    """

__all__ = tuple(exporting(__name__, ...))
