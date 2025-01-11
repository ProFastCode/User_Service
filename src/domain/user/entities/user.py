from dataclasses import dataclass
from typing import Self

from domain.common import AggregateRoot, UUIDEntity, CreatedAtEntity
from domain.user.value_objects.username import Username
from domain.user.value_objects.password import Password


@dataclass
class User(AggregateRoot, UUIDEntity, CreatedAtEntity):
    """
    Сущность пользователя.

    Атрибуты:
        id: Уникальный идентификатор пользователя.
        username: Имя пользователя (Value Object).
        password: Пароль пользователя (Value Object).
        email: Email пользователя.
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

    def check_password(self, password: str) -> bool:
        """
        Проверяет, совпадает ли переданный пароль с текущим паролем пользователя.
        """
        return self.password.to_raw() == password

    def change_password(self, new_password: str) -> None:
        """
        Изменяет текущий пароль пользователя на новый, проверяя его валидность.
        """
        self.password = Password(new_password)
