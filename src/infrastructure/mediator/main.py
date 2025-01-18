from dishka.async_container import AsyncContainer


from .mediator import Mediator
from src.application.user.commands import (
    LoginUser,
    LoginUserHandler,
    RegistrationUser,
    RegistrationUserHandler,
)
from src.application.user.queries import (
    GetUserByOid,
    GetUserByOidHandler,
    GetUserByUsername,
    GetUserByUsernameHandler,
)
from src.application.token.commands import (
    CreateTokenPair,
    CreateTokenPairHandler,
    CreateToken,
    CreateTokenHandler,
    RefreshToken,
    RefreshTokenHandler,
)
from src.application.token.queries import GetOidToken, GetOidTokenHandler


def init_mediator() -> Mediator:
    return Mediator()


async def setup_mediator(mediator: Mediator, container: AsyncContainer) -> None:
    mediator.register_command_handler(
        LoginUser,
        await container.get(LoginUserHandler),
    )
    mediator.register_command_handler(
        RegistrationUser,
        await container.get(RegistrationUserHandler),
    )
    mediator.register_query_handler(
        GetUserByOid,
        await container.get(GetUserByOidHandler),
    )
    mediator.register_query_handler(
        GetUserByUsername,
        await container.get(GetUserByUsernameHandler),
    )

    mediator.register_command_handler(
        CreateToken,
        await container.get(CreateTokenHandler),
    )
    mediator.register_command_handler(
        RefreshToken,
        await container.get(RefreshTokenHandler),
    )
    mediator.register_command_handler(
        CreateTokenPair,
        await container.get(CreateTokenPairHandler),
    )
    mediator.register_query_handler(
        GetOidToken,
        await container.get(GetOidTokenHandler),
    )
