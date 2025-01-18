import logging
from dataclasses import dataclass
from uuid import UUID
from time import time

import jwt

from src.config import Config
from src.infrastructure.mediator import Mediator
from src.application.token.dto import TokenPairDTO
from src.application.common.command import Command, CommandHandler
from src.application.token.constants import TokenType

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateTokenPair(Command[TokenPairDTO]):
    oid: UUID


class CreateTokenPairHandler(CommandHandler[CreateTokenPair, TokenPairDTO]):
    def __init__(
        self,
        config: Config,
        mediator: Mediator,
    ) -> None:
        self._config = config
        self._mediator = mediator

    async def __call__(self, command: CreateTokenPair) -> TokenPairDTO:
        oid = str(command.oid)
        current_time: float = time()

        access_token = jwt.encode(
            dict(oid=oid, exp=current_time + 60 * 10),
            self._config.JWT_SECRET,
            algorithm="HS256",
            headers=dict(tt=TokenType.ACCESS),
        )
        refresh_token = jwt.encode(
            dict(oid=oid, exp=current_time + 60 * 60 * 24),
            self._config.JWT_SECRET,
            algorithm="HS256",
            headers=dict(tt=TokenType.REFRESH),
        )

        token_pair_dto = TokenPairDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )

        logger.info(
            "Token pair created",
            extra={"access_token": access_token, "refresh_token": refresh_token},
        )

        return token_pair_dto
