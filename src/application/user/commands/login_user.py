import logging
from dataclasses import dataclass

from src.application.user.dto import AuthUserDTO
from src.config import Config
from src.infrastructure.mediator import Mediator
from src.application.user.queries import GetUserByUsername
from src.application.common.command import Command, CommandHandler
from src.domain.user.entities import User
from src.domain.user.value_objects import Token

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LoginUser(Command[AuthUserDTO]):
    username: str
    password: str


class LoginUserHandler(CommandHandler[LoginUser, AuthUserDTO]):
    def __init__(
        self,
        config: Config,
        mediator: Mediator,
    ) -> None:
        self._config = config
        self._mediator = mediator

    async def __call__(self, command: LoginUser) -> AuthUserDTO:
        user = await self._mediator.query(GetUserByUsername(command.username))
        user_entity = User.create(username=user.username, password=user.password)
        user_entity.check_password(command.password)

        access_token = Token.create(user.oid, 60 * 10, self._config.JWT_SECRET)
        refresh_token = Token.create(user.oid, 60 * 60 * 24, self._config.JWT_SECRET)

        auth_user_dto = AuthUserDTO(
            access_token=access_token.to_raw(),
            refresh_token=refresh_token.to_raw(),
        )

        logger.info(
            "User logged",
            extra={"access_token": access_token, "refresh_token": refresh_token},
        )

        return auth_user_dto
