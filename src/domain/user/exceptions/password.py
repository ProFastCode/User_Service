from dataclasses import dataclass

from src.domain.common import DomainError


@dataclass(eq=False)
class PasswordTooShortError(DomainError):
    password: str

    @property
    def message(self) -> str:
        return f"Пароль слишком короткий: {self.password}"


@dataclass(eq=False)
class PasswordTooLongError(DomainError):
    password: str

    @property
    def message(self) -> str:
        return f"Пароль слишком длинный: {self.password}"


@dataclass(eq=False)
class PasswordRequiresDigitError(DomainError):
    password: str

    @property
    def message(self) -> str:
        return f"Пароль должен содержать цифру: {self.password}"


@dataclass(eq=False)
class PasswordRequiresUppercaseError(DomainError):
    password: str

    @property
    def message(self) -> str:
        return f"Пароль должен содержать заглавную букву: {self.password}"


@dataclass(eq=False)
class PasswordRequiresLowercaseError(DomainError):
    password: str

    @property
    def message(self) -> str:
        return f"Пароль должен содержать строчную букву: {self.password}"


@dataclass(eq=False)
class PasswordRequiresSpecialCharError(DomainError):
    password: str

    @property
    def message(self) -> str:
        return f"Пароль должен содержать специальный символ: {self.password}"


@dataclass(eq=False)
class WrongPasswordFormatError(DomainError):
    password: str

    @property
    def message(self) -> str:
        return f"Неверный формат пароля: {self.password}"
