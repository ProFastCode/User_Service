from typing import Self
from dataclasses import dataclass

from src.domain.common import Entity
from src.domain.auth.value_objects.token import Token


@dataclass
class RefreshToken(Entity):
    token: Token

    @classmethod
    def create(cls, user_id: int, jwt_secret: str) -> Self:
        """
        Создает новый RefreshToken для указанного пользователя.

        :param user_id: Идентификатор пользователя.
        :return: Объект RefreshToken.
        """
        return cls(
            token=Token.create(
                user_id=user_id, expiration_time=60 * 60 * 24, jwt_secret=jwt_secret
            ),
        )
