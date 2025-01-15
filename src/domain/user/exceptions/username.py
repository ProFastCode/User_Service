from dataclasses import dataclass

from src.domain.common import DomainError


@dataclass(eq=False)
class UsernameTooShortError(DomainError):
    username: str

    @property
    def message(self) -> str:
        return f"Username too short {self.username}"


@dataclass(eq=False)
class UsernameTooLongError(DomainError):
    username: str

    @property
    def message(self) -> str:
        return f"Username too long {self.username}"


@dataclass(eq=False)
class WrongUsernameFormatError(DomainError):
    username: str

    @property
    def message(self) -> str:
        return f'Wrong username format "{self.username}"'
