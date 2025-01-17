import logging
from dataclasses import dataclass

from src.application.token.commands.create_token_pair import CreateTokenPair
from src.config import Config
from src.infrastructure.mediator import Mediator
from src.application.user.queries import GetUserByUsername
from src.application.common.command import Command, CommandHandler
from src.domain.user.entities import User
from src.application.token.dto import TokenPairDTO

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LoginUser(Command[TokenPairDTO]):
    username: str
    password: str


class LoginUserHandler(CommandHandler[LoginUser, TokenPairDTO]):
    def __init__(
        self,
        config: Config,
        mediator: Mediator,
    ) -> None:
        self._config = config
        self._mediator = mediator

    async def __call__(self, command: LoginUser) -> TokenPairDTO:
        user = await self._mediator.query(GetUserByUsername(command.username))
        user_entity = User.create(username=user.username, password=user.password)
        user_entity.check_password(command.password)

        token_pair_dto = await self._mediator.send(CreateTokenPair(user.oid))

        logger.info(
            "User logged",
            extra={
                "access_token": token_pair_dto.access_token,
                "refresh_token": token_pair_dto.refresh_token,
            },
        )

        return token_pair_dto
