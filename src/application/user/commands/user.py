import logging
from dataclasses import dataclass
from uuid import UUID

from infrastructure.mediator import Mediator

from application.common.command import Command, CommandHandler
from application.common.interfaces.uow import UnitOfWork
from application.user.interfaces import UserRepo
from domain.user.entities.user import User

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateUser(Command[UUID]):
    username: str
    password: str


class CreateUserHandler(CommandHandler[CreateUser, UUID]):
    def __init__(
        self,
        user_repo: UserRepo,
        uow: UnitOfWork,
        mediator: Mediator,
    ) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: CreateUser) -> UUID:
        user = User.create(command.username, command.password)
        await self._user_repo.create(user)
        events = user.pull_events()
        await self._mediator.publish(events)
        await self._uow.commit()

        logger.info("User created", extra={"user": user})

        return user.oid
