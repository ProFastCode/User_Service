from dataclasses import dataclass

from src.domain.common import ValueObjectError


@dataclass(eq=False)
class UsernameTooShortError(ValueObjectError):
    username: str

    @property
    def message(self) -> str:
        return f"Username too short {self.username}"


@dataclass(eq=False)
class UsernameTooLongError(ValueObjectError):
    username: str

    @property
    def message(self) -> str:
        return f"Username too long {self.username}"


@dataclass(eq=False)
class WrongUsernameFormatError(ValueObjectError):
    username: str

    @property
    def message(self) -> str:
        return f'Wrong username format "{self.username}"'
