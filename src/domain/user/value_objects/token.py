from typing import Self
from dataclasses import dataclass, field
from time import time
from uuid import UUID

import jwt

from src.domain.common import ValueObject
from src.domain.user.exceptions.value_objects.token import (
    TokenInvalidError,
    TokenExpiredError,
)


@dataclass(frozen=True)
class Token(ValueObject[str]):
    """
    Value Object для токена.

    Атрибуты:
        value: Строковое значение токена.
        payload: Полезная нагрузка токена.
    """

    value: str
    payload: dict = field(default_factory=dict, init=False)

    jwt_secret: str

    @classmethod
    def create(cls, user_oid: UUID, expiration_time: int, jwt_secret: str) -> Self:
        """
        Создает новый токен с указанным временем истечения.

        :param user_id: Идентификатор пользователя.
        :param expiration_time: Время истечения токена в секундах.
        :return: Экземпляр класса Token.
        """
        payload = {
            "user_oid": str(user_oid),
            "exp": int(time()) + expiration_time,
        }
        value = jwt.encode(payload, jwt_secret, algorithm="HS256")
        return cls(value=value, jwt_secret=jwt_secret)

    def _validate(self) -> None:
        """
        Проверяет валидность токена.

        :raises: TokenInvalidError, TokenExpiredError
        """
        try:
            payload = jwt.decode(self.value, self.jwt_secret, algorithms=["HS256"])
            object.__setattr__(self, "payload", payload)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.InvalidTokenError:
            raise TokenInvalidError()

        if not self.payload.get("exp") or not self.payload.get("user_oid"):
            raise TokenInvalidError()

    @property
    def is_valid(self) -> bool:
        """
        Проверяет валидность токена.

        :return: True, если токен валиден, иначе вызывает исключение.
        """
        self._validate()
        return True

    @property
    def user_oid(self) -> UUID:
        if user_oid := self.payload.get("user_oid"):
            return UUID(user_oid)

        raise TokenInvalidError(self.value, self.payload)
