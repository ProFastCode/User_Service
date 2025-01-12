from dishka import Provider, Scope, provide

from infrastructure.mediator import Mediator
from infrastructure.mediator.main import init_mediator
from infrastructure.uow import UnitOfWork
from infrastructure.memory.uow import MemoryUoW
from application.user.interfaces import UserRepo, UserReader
from infrastructure.memory import MemorySession
from infrastructure.memory.repositories import UserRepoMemory, UserReaderMemory
from application.user.commands import CreateUserHandler
from application.user.queries import GetUserByOidHandler


class AppProvider(Provider):
    create_user_handler = provide(CreateUserHandler, scope=Scope.REQUEST)
    get_user_by_oid_query_handler = provide(GetUserByOidHandler, scope=Scope.REQUEST)

    memory_storage = provide(MemorySession, scope=Scope.APP)

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
