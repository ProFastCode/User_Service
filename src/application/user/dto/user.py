from dataclasses import dataclass
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class CreateUserDTO(DTO):
    username: str
    password: str


@dataclass(frozen=True)
class UserDTO(DTO):
    oid: UUID
    username: str
    password: str
