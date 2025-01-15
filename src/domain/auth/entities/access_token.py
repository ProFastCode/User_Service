from typing import Self
from dataclasses import dataclass

from src.domain.common import Entity
from src.domain.auth.value_objects.token import Token


@dataclass
class AccessToken(Entity):
    token: Token

    @classmethod
    def create(cls, user_id: int) -> Self:
        """
        Создает новый AccessToken для указанного пользователя.

        :param user_id: Идентификатор пользователя.
        :return: Объект AccessToken.
        """
        return cls(
            token=Token.create(user_id, expiration_time=60 * 10),
        )
