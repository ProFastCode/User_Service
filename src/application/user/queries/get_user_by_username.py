import logging
from dataclasses import dataclass

from src.application.common.query import Query, QueryHandler
from src.application.user.interfaces import UserReader
from src.application.user import dto

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetUserByUsername(Query[dto.UserDTO]):
    username: str


class GetUserByUsernameHandler(QueryHandler[GetUserByUsername, dto.UserDTO]):
    def __init__(self, user_reader: UserReader) -> None:
        self._user_reader = user_reader

    async def __call__(self, query: GetUserByUsername) -> dto.UserDTO:
        user = await self._user_reader.get_by_username(query.username)
        logger.debug(
            "Get user by username", extra={"username": query.username, "user": user}
        )
        return user