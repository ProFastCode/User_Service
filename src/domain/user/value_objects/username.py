import re
from dataclasses import dataclass

from domain.common import ValueObject
from domain.user.exceptions.username import (
    UsernameTooShortError,
    UsernameTooLongError,
    WrongUsernameFormatError,
)


MIN_USERNAME_LENGTH = 4
MAX_USERNAME_LENGTH = 32
USERNAME_PATTERN = re.compile(r"[A-Za-z][A-Za-z1-9_]+")


@dataclass(frozen=True)
class Username(ValueObject[str]):
    """
    Value Object для имени пользователя.

    Правила валидации:
    - Длина имени пользователя должна быть от MIN_USERNAME_LENGTH до MAX_USERNAME_LENGTH.
    - Имя пользователя должно начинаться с буквы и может содержать только буквы, цифры и символы подчеркивания.
    """

    value: str

    def _validate(self) -> None:
        if len(self.value) < MIN_USERNAME_LENGTH:
            raise UsernameTooShortError(self.value)
        elif len(self.value) > MAX_USERNAME_LENGTH:
            raise UsernameTooLongError(self.value)
        elif not USERNAME_PATTERN.match(self.value):
            raise WrongUsernameFormatError(self.value)
