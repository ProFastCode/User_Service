from dataclasses import dataclass
from typing import Self

from src.domain.common import AggregateRoot, CreatedAtEntity, UUIDEntity
from src.domain.user.exceptions.entities.user import \
    InvalidUsernameOrPasswordError
from src.domain.user.value_objects import Password, Username


@dataclass
class User(AggregateRoot, UUIDEntity, CreatedAtEntity):
    """
    Сущность пользователя.

    Атрибуты:
        id: Уникальный идентификатор пользователя.
        username: Имя пользователя (Value Object).
        password: Пароль пользователя (Value Object).
        created_at: Дата регистрации пользователя.
    """

    username: Username
    password: Password

    @classmethod
    def create(cls, username: str, password: str) -> Self:
        """
        Создает нового пользователя с уникальным идентификатором и текущей датой регистрации.
        """
        return cls(
            username=Username(username),
            password=Password(password),
        )

    def check_password(self, password: str):
        """
        Проверяет, совпадает ли переданный пароль с текущим паролем пользователя.
        """
        if self.password.to_raw() != password:
            raise InvalidUsernameOrPasswordError(
                username=self.username.to_raw(), password=password
            )

    def change_password(self, new_password: str) -> None:
        """
        Изменяет текущий пароль пользователя на новый, проверяя его валидность.
        """
        self.password = Password(new_password)
