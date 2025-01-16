from dishka.async_container import AsyncContainer


from .mediator import Mediator
from src.application.user.commands import (
    CreateUser,
    CreateUserHandler,
    LoginUser,
    LoginUserHandler,
)
from src.application.user.queries import (
    GetUserByOid,
    GetUserByOidHandler,
    GetUserByToken,
    GetUserByTokenHandler,
    GetUserByUsername,
    GetUserByUsernameHandler,
)


def init_mediator() -> Mediator:
    return Mediator()


async def setup_mediator(mediator: Mediator, container: AsyncContainer) -> None:
    mediator.register_command_handler(
        LoginUser,
        await container.get(LoginUserHandler),
    )
    mediator.register_command_handler(
        CreateUser,
        await container.get(CreateUserHandler),
    )

    mediator.register_query_handler(
        GetUserByOid,
        await container.get(GetUserByOidHandler),
    )
    mediator.register_query_handler(
        GetUserByToken,
        await container.get(GetUserByTokenHandler),
    )
    mediator.register_query_handler(
        GetUserByUsername,
        await container.get(GetUserByUsernameHandler),
    )
