from dataclasses import dataclass

from src.domain.common import ValueObjectError


@dataclass(eq=False)
class TokenInvalidError(ValueObjectError):
    token: str
    payload: dict

    @property
    def message(self) -> str:
        return f"Token invalid {self.token}"


@dataclass(eq=False)
class TokenExpiredError(ValueObjectError):
    token: str
    payload: dict

    @property
    def message(self) -> str:
        return f"Token expired {self.token}"
