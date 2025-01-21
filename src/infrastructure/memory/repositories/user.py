from uuid import UUID

from src.application.user import dto
from src.application.user.interfaces import UserReader, UserRepo
from src.domain.user.entities.user import User

from .base import MemoryRepo


class UserRepoMemory(MemoryRepo, UserRepo):
    _storage: list[User]

    async def create(self, user: User) -> UUID:
        self._storage.append(user)
        return user.oid

    async def delete_by_oid(self, user_oid: UUID) -> None:
        for user in self._storage:
            if user.oid == user_oid:
                self._storage.remove(user)


class UserReaderMemory(MemoryRepo, UserReader):
    _storage: list[User]

    async def get_by_oid(self, user_oid: UUID) -> dto.UserDTO:
        for user in self._storage:
            if user.oid == user_oid:
                return dto.UserDTO(
                    oid=user.oid,
                    username=user.username.to_raw(),
                    password=user.password.to_raw(),
                )

        raise ValueError(user_oid)

    async def get_by_username(self, username: str) -> dto.UserDTO:
        for user in self._storage:
            if user.username.to_raw() == username:
                return dto.UserDTO(
                    oid=user.oid,
                    username=user.username.to_raw(),
                    password=user.password.to_raw(),
                )

        raise KeyError()
