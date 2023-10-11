"""Credential interface type"""

from pydantic import SecretStr

class Credential(SecretStr):

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.get_secret_value() == other
        elif isinstance(other, SecretStr):
            return self.get_secret_value() == other.get_secret_value()
        else:
            return super().__eq__(other)


__all__ = ("Credential",)
