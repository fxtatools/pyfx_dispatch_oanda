"""Credential interface type"""


from contextvars import ContextVar
from pydantic import SecretStr
from typing import Optional
from typing_extensions import Self
from zope.password.interfaces import IPasswordManager  # type: ignore [import-untyped]

shadow_encoder: ContextVar[IPasswordManager] = ContextVar("shadow_encoder")


class Credential(SecretStr):

    __slots__ = ("_secret_value", "_shadow_value",)

    _shadow_value: bytes

    def get_shadow_value(self, encoder: Optional[IPasswordManager] = None) -> bytes:
        if hasattr(self, "_shadow_value"):
            return self._shadow_value
        else:
            enc = shadow_encoder.get() if encoder is None else encoder
            encoded = enc.encodePassword(self.get_secret_value())
            self._shadow_value = encoded
            return encoded

    @classmethod
    def create_shadowed(cls, shadow_value: bytes) -> Self:
        inst = cls('')
        inst._shadow_value = shadow_value
        return inst

    def shadowed(self) -> bool:
        return hasattr(self, "_shadow_value")

    def __repr__(self) -> str:
        if self.shadowed():
            return self.__class__.__name__ + "(shadowed:" + str(self._shadow_value) + ")"
        else:
            return super().__repr__()

    def __hash__(self) -> int:
        clsname = self.__class__.__name__
        if self.shadowed():
            return hash((clsname, self._shadow_value, True,))
        else:
            try:
                encoder = shadow_encoder.get()
            except LookupError:
                #
                # producing a unique hash code, when the
                # _shadow_value cannot be determined
                #
                return hash((clsname, self._secret_value, False,))
            else:
                return hash((clsname, self.get_shadow_value(encoder), True,))

    def __eq__(self, other) -> bool:
        if id(self) is id(other):
            return True
        elif isinstance(other, str):
            return self._secret_value == other
        elif isinstance(other, Credential) and self.shadowed() and other.shadowed():
            return self._shadow_value == other._shadow_value
        elif isinstance(other, SecretStr):
            return self._secret_value == other.get_secret_value()
        else:
            return super().__eq__(other)

    def __bytes__(self):
        if hasattr(self, "_bytes"):
            return self._bytes
        else:
            b = self.get_secret_value().encode()
            self._bytes = b
            return b

    def __getstate__(self) -> tuple:
        # ensure the credential's text value will not be included
        # in serialization, e.g in applications of ZODB
        if self.shadowed():
            return (self._shadow_value,)
        elif hasattr(self, "_secret_value"):
            ## may throw LookupError if no shadow_encoder was initialized
            ## to the ContextVar, in the current thread
            ##
            ## The shadow_encoder value may be initialized for worker threads
            ## and the main thread under StorageController and subclasses
            ##
            shadowed = self.get_shadow_value()
            return (shadowed,)
        else:
            return ()

    def __setstate__(self, state: tuple):
        if len(state) == 0:
            self._shadow_value = b''
        else:
            self._shadow_value = state[0]
        self._secret_value = ''


__all__ = ("Credential", "shadow_encoder")
