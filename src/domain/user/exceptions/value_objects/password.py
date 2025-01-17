from dataclasses import dataclass

from src.domain.common import ValueObjectError


@dataclass(eq=False)
class PasswordTooShortError(ValueObjectError):
    status = 422
    password: str

    @property
    def message(self) -> str:
        return f"Password is too short: {self.password}"


@dataclass(eq=False)
class PasswordTooLongError(ValueObjectError):
    status = 422
    password: str

    @property
    def message(self) -> str:
        return f"Password is too long: {self.password}"


@dataclass(eq=False)
class PasswordRequiresDigitError(ValueObjectError):
    status = 422
    password: str

    @property
    def message(self) -> str:
        return f"Password must contain a digit: {self.password}"


@dataclass(eq=False)
class PasswordRequiresUppercaseError(ValueObjectError):
    status = 422
    password: str

    @property
    def message(self) -> str:
        return f"Password must contain an uppercase letter: {self.password}"


@dataclass(eq=False)
class PasswordRequiresLowercaseError(ValueObjectError):
    status = 422
    password: str

    @property
    def message(self) -> str:
        return f"Password must contain a lowercase letter: {self.password}"


@dataclass(eq=False)
class PasswordRequiresSpecialCharError(ValueObjectError):
    status = 422
    password: str

    @property
    def message(self) -> str:
        return f"Password must contain a special character: {self.password}"


@dataclass(eq=False)
class WrongPasswordFormatError(ValueObjectError):
    status = 422
    password: str

    @property
    def message(self) -> str:
        return f"Invalid password format: {self.password}"
