import logging
from dataclasses import dataclass

from src.application.common.command import Command, CommandHandler
from src.application.token.commands.create_token import CreateToken
from src.application.token.constants import TokenType
from src.application.token.dto import TokenDTO
from src.application.token.queries.get_oid_token import GetOidToken
from src.config import Config
from src.infrastructure.mediator import Mediator

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RefreshToken(Command[TokenDTO]):
    token: str


class RefreshTokenHandler(CommandHandler[RefreshToken, TokenDTO]):
    def __init__(
        self,
        config: Config,
        mediator: Mediator,
    ) -> None:
        self._config = config
        self._mediator = mediator

    async def __call__(self, command: RefreshToken) -> TokenDTO:
        oid = await self._mediator.query(GetOidToken(command.token, TokenType.REFRESH))
        token_dto = await self._mediator.send(
            CreateToken(oid=oid, token_type=TokenType.ACCESS, seconds_life=60 * 10)
        )

        logger.info(
            "Token refreshed",
            extra={"token": token_dto},
        )

        return token_dto
