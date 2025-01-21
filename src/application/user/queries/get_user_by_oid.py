import logging
from dataclasses import dataclass
from uuid import UUID

from src.application.common.query import Query, QueryHandler
from src.application.user import dto
from src.application.user.interfaces import UserReader

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetUserByOid(Query[dto.UserDTO]):
    user_oid: UUID


class GetUserByOidHandler(QueryHandler[GetUserByOid, dto.UserDTO]):
    def __init__(self, user_reader: UserReader) -> None:
        self._user_reader = user_reader

    async def __call__(self, query: GetUserByOid) -> dto.UserDTO:
        user = await self._user_reader.get_by_oid(query.user_oid)
        logger.debug(
            "Get user by oid", extra={"user_oid": query.user_oid, "user": user}
        )
        return user
