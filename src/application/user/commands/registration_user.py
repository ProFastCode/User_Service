import logging
from dataclasses import dataclass

from src.application.user.dto import AuthUserDTO
from src.config import Config
from src.domain.user.value_objects import Token
from src.infrastructure.mediator import Mediator
from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces import UserRepo
from src.domain.user.entities.user import User

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RegistrationUser(Command[AuthUserDTO]):
    username: str
    password: str


class RegistrationUserHandler(CommandHandler[RegistrationUser, AuthUserDTO]):
    def __init__(
        self,
        config: Config,
        user_repo: UserRepo,
        uow: UnitOfWork,
        mediator: Mediator,
    ) -> None:
        self._config = config
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: RegistrationUser) -> AuthUserDTO:
        user = User.create(command.username, command.password)
        await self._user_repo.create(user)
        events = user.pull_events()
        await self._mediator.publish(events)
        await self._uow.commit()

        access_token = Token.create(user.oid, 60 * 10, self._config.JWT_SECRET)
        refresh_token = Token.create(user.oid, 60 * 60 * 24, self._config.JWT_SECRET)

        auth_user_dto = AuthUserDTO(
            access_token=access_token.to_raw(),
            refresh_token=refresh_token.to_raw(),
        )

        logger.info("User registered", extra={"user": user})

        return auth_user_dto
