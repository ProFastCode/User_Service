from dataclasses import dataclass

from src.domain.common import ValueObjectError


@dataclass(eq=False)
class PasswordTooShortError(ValueObjectError):
    password: str

    @property
    def message(self) -> str:
        return f"Пароль слишком короткий: {self.password}"


@dataclass(eq=False)
class PasswordTooLongError(ValueObjectError):
    password: str

    @property
    def message(self) -> str:
        return f"Пароль слишком длинный: {self.password}"


@dataclass(eq=False)
class PasswordRequiresDigitError(ValueObjectError):
    password: str

    @property
    def message(self) -> str:
        return f"Пароль должен содержать цифру: {self.password}"


@dataclass(eq=False)
class PasswordRequiresUppercaseError(ValueObjectError):
    password: str

    @property
    def message(self) -> str:
        return f"Пароль должен содержать заглавную букву: {self.password}"


@dataclass(eq=False)
class PasswordRequiresLowercaseError(ValueObjectError):
    password: str

    @property
    def message(self) -> str:
        return f"Пароль должен содержать строчную букву: {self.password}"


@dataclass(eq=False)
class PasswordRequiresSpecialCharError(ValueObjectError):
    password: str

    @property
    def message(self) -> str:
        return f"Пароль должен содержать специальный символ: {self.password}"


@dataclass(eq=False)
class WrongPasswordFormatError(ValueObjectError):
    password: str

    @property
    def message(self) -> str:
        return f"Неверный формат пароля: {self.password}"
