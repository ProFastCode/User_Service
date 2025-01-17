from dataclasses import dataclass

from src.domain.common import ValueObjectError


@dataclass(eq=False)
class TokenInvalidError(ValueObjectError):
    status = 401

    @property
    def message(self) -> str:
        return "The provided token is invalid or malformed."


@dataclass(eq=False)
class TokenExpiredError(ValueObjectError):
    status = 401

    @property
    def message(self) -> str:
        return "The provided token has expired and is no longer valid."
