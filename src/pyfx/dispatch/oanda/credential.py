"""Credential interface type"""

import immutables
from pydantic import SecretStr
from typing import Any, Mapping


class Credential(SecretStr):

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.get_secret_value() == other
        elif isinstance(other, SecretStr):
            return self.get_secret_value() == other.get_secret_value()
        else:
            return super().__eq__(other)

    def __bytes__(self):
        if hasattr(self, "_bytes"):
            return self._bytes
        else:
            b = self.get_secret_value().encode()
            self._bytes = b
            return b

    def __getstate__(self) -> immutables.Map[str, str]:
        # ensure the credential's text value will not be included
        # in serialization, e.g in applications of ZODB
        return immutables.Map()

    def __setstate__(self, state: Mapping[str, Any]):
        if '_secret_value' in state:
            self._secret_value = state['_secret_value']
        else:
            self._secret_value = ''



__all__ = ("Credential",)
