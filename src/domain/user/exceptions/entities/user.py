from dataclasses import dataclass

from src.domain.common import DomainError


@dataclass(eq=False)
class InvalidUsernameOrPasswordError(DomainError):
    status = 401

    username: str
    password: str

    @property
    def message(self) -> str:
        return f"Неверное имя пользователя или пароль: {self.username} {self.password}"
