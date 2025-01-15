from typing import Protocol
from uuid import UUID

from src.application.user import dto


class UserReader(Protocol):
    async def get_by_oid(self, user_oid: UUID) -> dto.UserDTO:
        raise NotImplementedError
