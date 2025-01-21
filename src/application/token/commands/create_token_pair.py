import logging
from dataclasses import dataclass
from uuid import UUID

from src.application.common.command import Command, CommandHandler
from src.application.token.commands import CreateToken
from src.application.token.constants import TokenType
from src.application.token.dto import TokenPairDTO
from src.config import Config
from src.infrastructure.mediator import Mediator

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
        access_token = await self._mediator.send(
            CreateToken(command.oid, TokenType.ACCESS, 60 * 10)
        )
        refresh_token = await self._mediator.send(
            CreateToken(command.oid, TokenType.REFRESH, 60 * 60 * 24)
        )

        token_pair_dto = TokenPairDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )

        logger.info(
            "Token pair created",
            extra={"token_pair": token_pair_dto},
        )

        return token_pair_dto
