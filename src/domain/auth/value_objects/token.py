from typing import Self
from dataclasses import dataclass
from time import time

import jwt

from src.domain.common import ValueObject
from src.domain.auth.exceptions.token import TokenInvalidError, TokenExpiredError

JWT_SECRET = "your_secret_key"  # Замените на секретный ключ из конфигурации


@dataclass(frozen=True)
class Token(ValueObject[str]):
    """
    Value Object для токена.

    Атрибуты:
        value: Строковое значение токена.
    """

    value: str

    @classmethod
    def create(cls, user_id: int, expiration_time: int) -> Self:
        """
        Создает новый токен с указанным временем истечения.

        :param user_id: Идентификатор пользователя.
        :param expiration_time: Время истечения токена в секундах.
        :return: Строковое значение токена.
        """
        payload = {
            "user_id": user_id,
            "exp": int(time()) + expiration_time,
        }
        value = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        token = cls(value)
        return token

    def _validate(self) -> None:
        """
        Проверяет валидность токена.

        :raises: TokenInvalidError, TokenExpiredError
        """
        try:
            payload = jwt.decode(self.value, JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError(self.value)
        except jwt.InvalidTokenError:
            raise TokenInvalidError(self.value)

        if not (exp := payload.get("exp")) or not payload.get("user_id"):
            raise TokenInvalidError(self.value)

        if exp < int(time()):
            raise TokenExpiredError(self.value)
