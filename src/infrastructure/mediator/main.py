from dishka.async_container import AsyncContainer

from .mediator import Mediator
from application.user.commands import CreateUser, CreateUserHandler
from application.user.queries import GetUserByOid, GetUserByOidHandler


def init_mediator() -> Mediator:
    mediator = Mediator()
    return mediator


async def setup_mediator(mediator: Mediator, container: AsyncContainer) -> None:
    mediator.register_command_handler(
        CreateUser,
        await container.get(CreateUserHandler),
    )
    mediator.register_query_handler(
        GetUserByOid,
        await container.get(GetUserByOidHandler),
    )
