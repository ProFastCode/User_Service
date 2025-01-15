from dataclasses import dataclass

from src.domain.common import DomainError


@dataclass(eq=False)
class TokenInvalidError(DomainError):
    token: str

    @property
    def message(self) -> str:
        return f"Token invalid {self.token}"


@dataclass(eq=False)
class TokenExpiredError(DomainError):
    token: str

    @property
    def message(self) -> str:
        return f"Token expired {self.token}"
