import logging
from dataclasses import dataclass

from src.application.common.query import Query, QueryHandler
from src.application.user.interfaces import UserReader
from src.application.user import dto
from src.domain.user.value_objects import Token
from src.config import Config

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetUserByToken(Query[dto.UserDTO]):
    access_token: str


class GetUserByTokenHandler(QueryHandler[GetUserByToken, dto.UserDTO]):
    def __init__(self, user_reader: UserReader, config: Config) -> None:
        self._config = config
        self._user_reader = user_reader

    async def __call__(self, query: GetUserByToken) -> dto.UserDTO:
        access_token = Token(query.access_token, self._config.JWT_SECRET)
        user = await self._user_reader.get_by_oid(access_token.user_oid)
        logger.debug(
            "Get user by oid",
            extra={"user_oid": access_token.user_oid, "user": user},
        )
        return user
