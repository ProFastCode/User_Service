from dataclasses import dataclass

from application.common.dto import DTO


@dataclass(frozen=True)
class CreateUserDTO(DTO):
    username: str
    password: str


@dataclass(frozen=True)
class UserDTO(DTO):
    username: str
