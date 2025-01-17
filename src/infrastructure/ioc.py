from dishka import Provider, Scope, provide

from src.config import Config
from src.infrastructure.mediator import Mediator
from src.infrastructure.mediator.main import init_mediator
from src.infrastructure.uow import UnitOfWork
from src.infrastructure.memory.uow import MemoryUoW
from src.application.user.interfaces import UserRepo, UserReader
from src.infrastructure.memory import MemorySession
from src.infrastructure.memory.repositories import UserRepoMemory, UserReaderMemory
from src.application.user.commands import RegistrationUserHandler, LoginUserHandler
from src.application.user.queries import (
    GetUserByOidHandler,
    GetUserByTokenHandler,
    GetUserByUsernameHandler,
)


class AppProvider(Provider):
    config = provide(Config, scope=Scope.APP)

    memory_storage = provide(MemorySession, scope=Scope.APP)

    login_user_command_handler = provide(LoginUserHandler, scope=Scope.REQUEST)
    registration_user_command_handler = provide(
        RegistrationUserHandler, scope=Scope.REQUEST
    )

    get_user_by_oid_query_handler = provide(GetUserByOidHandler, scope=Scope.REQUEST)
    get_user_by_token_query_handler = provide(
        GetUserByTokenHandler, scope=Scope.REQUEST
    )
    get_user_by_username_query_handler = provide(
        GetUserByUsernameHandler, scope=Scope.REQUEST
    )

    @provide(scope=Scope.REQUEST)
    def uow(self) -> UnitOfWork:
        return MemoryUoW()

    @provide(scope=Scope.APP)
    def user_repo(self, session: MemorySession) -> UserRepo:
        return UserRepoMemory(storage=session.storage)

    @provide(scope=Scope.APP)
    def user_reader(self, session: MemorySession) -> UserReader:
        return UserReaderMemory(storage=session.storage)

    @provide(scope=Scope.REQUEST)
    async def mediator(self) -> Mediator:
        return init_mediator()
