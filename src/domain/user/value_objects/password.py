import re
from dataclasses import dataclass

from src.domain.common import ValueObject
from src.domain.user.exceptions.value_objects.password import (
    PasswordTooShortError,
    PasswordTooLongError,
    PasswordRequiresDigitError,
    PasswordRequiresUppercaseError,
    PasswordRequiresLowercaseError,
    PasswordRequiresSpecialCharError,
    WrongPasswordFormatError,
)

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 64
PASSWORD_PATTERN = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,64}$"
)


@dataclass(frozen=True)
class Password(ValueObject[str]):
    """
    Value Object для пароля.

    Правила валидации:
    - Длина пароля должна быть от MIN_PASSWORD_LENGTH до MAX_PASSWORD_LENGTH.
    - Пароль должен содержать:
      - Хотя бы одну цифру.
      - Хотя бы одну заглавную букву.
      - Хотя бы одну строчную букву.
      - Хотя бы один специальный символ (@$!%*?&).
    - Пароль должен соответствовать регулярному выражению PASSWORD_PATTERN.
    """

    value: str

    def _validate(self) -> None:
        """
        Проверяет валидность пароля.

        :raises: PasswordTooShortError, PasswordTooLongError, PasswordRequiresDigitError,
                 PasswordRequiresUppercaseError, PasswordRequiresLowercaseError,
                 PasswordRequiresSpecialCharError, WrongPasswordFormatError
        """
        if len(self.value) < MIN_PASSWORD_LENGTH:
            raise PasswordTooShortError(self.value)
        elif len(self.value) > MAX_PASSWORD_LENGTH:
            raise PasswordTooLongError(self.value)
        elif not re.search(r"\d", self.value):
            raise PasswordRequiresDigitError(self.value)
        elif not re.search(r"[A-Z]", self.value):
            raise PasswordRequiresUppercaseError(self.value)
        elif not re.search(r"[a-z]", self.value):
            raise PasswordRequiresLowercaseError(self.value)
        elif not re.search(r"[@$!%*?&]", self.value):
            raise PasswordRequiresSpecialCharError(self.value)
        elif not PASSWORD_PATTERN.match(self.value):
            raise WrongPasswordFormatError(self.value)
