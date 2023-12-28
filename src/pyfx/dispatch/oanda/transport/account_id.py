"""Common AccountId transport type"""

from typing import TYPE_CHECKING
from typing_extensions import ClassVar, Self

from ..credential import Credential, shadow_encoder
from .transport_base import TransportSecretStr, TransportSecretStrType

if TYPE_CHECKING:
    _ = shadow_encoder


class AccountId(Credential, TransportSecretStr):
    """
    Account identifier

    Transport encoding: String
    Storage class: Credential

    ## Configuration Management

    The Configuration API provides a primary management interface for
    AccountId settings and other configuration properties. This is
    managed via a Configuration Profile API, extensional to the
    base ConfigurationModel. In this context, an AccountId would
    generally be initialized from a configuration file within an
    application storage directory.

    ## Storage Encoding

    The AccountId transport type is implemented as a subclass of
    Credential. When a Credential object is first processed for
    persistent storage, the "Secret String" value for the object
    will be shadowed  with a unique hash string, produced with e.g
    an `SHA1` string encoding.  Similar to a file-based password
    storage system for UNIX hosts, this hash string will then be
    stored within the persistent state object, rather than storing
    the original "Secret String" value.

    In application, this requires the presence of a password
    encoder implementing `IPasswordManager` (from `zope.password`),
    such that the encoder will be initialized and set as the value
    of the `shadow_encoder` context variable (from the `credential`
    module) within the currrent thread.

    This effective thread-local binding for `shadow_encoder` will
    allow for the encoder to be accessed within `__getstate__()`,
    at the time when each AccountId object is processed for
    persistent storage. The StorageController  API will ensure
    that this context variable is bound within  each worker
    thread for the controller's thread pool exeuctor.

    Subsequent of reinitialization from persistent storage, each
    AcountId object can be matched to the original AccountId,
    using the password hash produced for each.

    The "Shadow" password hash will be stored as a `bytes` value,
    available via the method `Credential.get_shadow_value()`,
    similarly via `AccountId.get_shadow_value()`. In fact, this
    method is where a `shadow_encoder` is required, for when
    the `AccountId` object does not have an initialized "Shadow"
    value.
    """

    storage_class: ClassVar[type] = Credential
    storage_type: ClassVar[type] = Credential
    ## recusive on dereference:
    # storage_class:  ClassVar[type] = "AccountId"
    # storage_type: ClassVar[type] = "AccountId"
    hash_code: int

    @classmethod
    def create_deferred(cls) -> Self:
        """Create an uninitialized AccountId

        The AccountId object will be initialized with an empty string
        as the object's "Secret String" value. This value may be
        reinitialized with a call to `__setstate__(state)`, provided
        with a `state` object such as from the `__getstate__()` method
        applied to an initialized AccountId.
        """
        return cls('')

    def deferred(self) -> bool:
        return len(self._secret_value) == 0 if hasattr(self, "_secret_value") else True

    def __repr__(self) -> str:
        if self.deferred() and not self.shadowed():
            return self.__class__.__name__ + "(<deferred>)"
        else:
            return super().__repr__()


__all__ = "AccountId",
