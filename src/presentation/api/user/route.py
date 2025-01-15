from typing import Annotated
from uuid import UUID

from litestar.params import Body
from litestar import post, get, Router
from dishka.integrations.litestar import inject, FromDishka

from src.application.user.commands.user import CreateUser
from src.application.user.queries.user import GetUserByOid
from src.application.user.dto.user import UserDTO, CreateUserDTO
from src.infrastructure.mediator.mediator import Mediator


@get()
@inject
async def read(user_uid: UUID, mediator: FromDishka[Mediator]) -> UserDTO:
    return await mediator.query(GetUserByOid(user_uid))


@post()
@inject
async def create(
    data: Annotated[CreateUserDTO, Body()], mediator: FromDishka[Mediator]
) -> UUID:
    return await mediator.send(
        CreateUser(username=data.username, password=data.password)
    )


router = Router("/users", tags=["users"], route_handlers=[read, create])
