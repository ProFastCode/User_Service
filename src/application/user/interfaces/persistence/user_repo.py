from typing import Protocol
from uuid import UUID

from src.domain.user.entities.user import UserEntity


class UserRepo(Protocol):
    async def create(self, user: UserEntity) -> UUID:
        raise NotImplementedError

    async def delete_by_oid(self, user_oid: UUID) -> None:
        raise NotImplementedError
