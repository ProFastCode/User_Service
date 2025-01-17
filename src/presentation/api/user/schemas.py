from dataclasses import dataclass
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class ResponseUserDTO(DTO):
    oid: UUID
    username: str
