import logging
from dataclasses import dataclass

from src.application.user.dto import LoginUserDTO
from src.config import Config
from src.infrastructure.mediator import Mediator
from src.application.user.queries import GetUserByUsername
from src.application.common.command import Command, CommandHandler
from src.domain.user.entities import User
from src.domain.user.value_objects import Token

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LoginUser(Command[LoginUserDTO]):
    username: str
    password: str


class LoginUserHandler(CommandHandler[LoginUser, LoginUserDTO]):
    def __init__(
        self,
        mediator: Mediator,
        config: Config,
    ) -> None:
        self._config = config
        self._mediator = mediator

    async def __call__(self, command: LoginUser) -> LoginUserDTO:
        user = await self._mediator.query(GetUserByUsername(command.username))
        user_entity = User.create(username=user.username, password=user.password)
        user_entity.check_password(command.password)

        access_token = Token.create(user.oid, 60 * 10, self._config.JWT_SECRET)
        refresh_token = Token.create(user.oid, 60 * 60 * 24, self._config.JWT_SECRET)

        login_user_dto = LoginUserDTO(
            access_token=access_token.to_raw(),
            refresh_token=refresh_token.to_raw(),
        )

        logger.info(
            "Auth token pair created",
            extra={"access_token": access_token, "refresh_token": refresh_token},
        )

        return login_user_dto
