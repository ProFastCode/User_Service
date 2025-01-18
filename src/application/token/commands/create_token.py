import logging
from dataclasses import dataclass
from uuid import UUID
from time import time

import jwt

from src.config import Config
from src.infrastructure.mediator import Mediator
from src.application.common.command import Command, CommandHandler
from src.application.token.constants import TokenType
from src.application.token.dto import TokenDTO

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateToken(Command[TokenDTO]):
    oid: UUID
    token_type: TokenType
    seconds_life: int


class CreateTokenHandler(CommandHandler[CreateToken, TokenDTO]):
    def __init__(
        self,
        config: Config,
        mediator: Mediator,
    ) -> None:
        self._config = config
        self._mediator = mediator

    async def __call__(self, command: CreateToken) -> TokenDTO:
        exp: float = time() + command.seconds_life

        token = jwt.encode(
            dict(oid=str(command.oid), exp=exp),
            self._config.JWT_SECRET,
            algorithm="HS256",
            headers=dict(tt=command.token_type),
        )

        token_dto = TokenDTO(
            token=token,
            exp=exp,
            token_type=command.token_type,
        )

        logger.info(
            "Token created",
            extra={"token": token_dto},
        )

        return token_dto
