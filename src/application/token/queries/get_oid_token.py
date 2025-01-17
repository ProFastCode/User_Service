import logging
from dataclasses import dataclass
from uuid import UUID

import jwt

from src.config import Config
from src.infrastructure.mediator import Mediator
from src.application.common.query import Query, QueryHandler
from src.application.token.exceptions.token import TokenExpiredError, TokenInvalidError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetOidToken(Query[UUID]):
    token: str


class GetOidTokenHandler(QueryHandler[GetOidToken, UUID]):
    def __init__(
        self,
        config: Config,
        mediator: Mediator,
    ) -> None:
        self._config = config
        self._mediator = mediator

    async def __call__(self, query: GetOidToken) -> UUID:
        try:
            payload = jwt.decode(
                query.token, self._config.JWT_SECRET, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.InvalidTokenError:
            raise TokenInvalidError()

        if not payload.get("exp") or not payload.get("oid"):
            raise TokenInvalidError()

        oid = UUID(payload.get("oid"))

        logger.info(
            "Oid token received",
            extra={"payload": payload},
        )

        return oid
