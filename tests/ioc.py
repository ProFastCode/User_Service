from dishka import Provider, Scope, provide

from src.application.token.commands import (CreateTokenHandler,
                                            CreateTokenPairHandler,
                                            RefreshTokenHandler)
from src.application.token.queries import GetOidTokenHandler
from src.application.user.commands import (LoginUserHandler,
                                           RegistrationUserHandler)
from src.application.user.interfaces import UserReader, UserRepo
from src.application.user.queries import (GetUserByOidHandler,
                                          GetUserByUsernameHandler)
from src.config import Config
from src.infrastructure.mediator import Mediator
from src.infrastructure.mediator.main import init_mediator
from src.infrastructure.memory import MemorySession
from src.infrastructure.memory.repositories import (UserReaderMemory,
                                                    UserRepoMemory)
from src.infrastructure.memory.uow import MemoryUoW
from src.infrastructure.uow import UnitOfWork


class TestAppProvider(Provider):
    config = provide(Config, scope=Scope.APP)

    memory_storage = provide(MemorySession, scope=Scope.APP)

    login_user_command_handler = provide(LoginUserHandler, scope=Scope.REQUEST)
    registration_user_command_handler = provide(
        RegistrationUserHandler, scope=Scope.REQUEST
    )
    get_user_by_oid_query_handler = provide(GetUserByOidHandler, scope=Scope.REQUEST)
    get_user_by_username_query_handler = provide(
        GetUserByUsernameHandler, scope=Scope.REQUEST
    )

    create_token_command_handler = provide(CreateTokenHandler, scope=Scope.REQUEST)
    refresh_token_command_handler = provide(RefreshTokenHandler, scope=Scope.REQUEST)
    create_token_pair_command_handler = provide(
        CreateTokenPairHandler, scope=Scope.REQUEST
    )
    get_oid_token_query_handler = provide(GetOidTokenHandler, scope=Scope.REQUEST)

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
