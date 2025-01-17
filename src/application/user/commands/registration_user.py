import logging
from dataclasses import dataclass

from src.config import Config
from src.infrastructure.mediator import Mediator
from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces import UserRepo
from src.domain.user.entities.user import User
from src.application.token.commands import CreateTokenPair
from src.application.token.dto import TokenPairDTO

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RegistrationUser(Command[TokenPairDTO]):
    username: str
    password: str


class RegistrationUserHandler(CommandHandler[RegistrationUser, TokenPairDTO]):
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

    async def __call__(self, command: RegistrationUser) -> TokenPairDTO:
        user = User.create(command.username, command.password)
        await self._user_repo.create(user)
        events = user.pull_events()
        await self._mediator.publish(events)
        await self._uow.commit()

        token_pair_dto = await self._mediator.send(CreateTokenPair(user.oid))

        logger.info("User registered", extra={"user": user})

        return token_pair_dto
