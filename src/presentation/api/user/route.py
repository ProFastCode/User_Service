from typing import Annotated
from uuid import UUID
from dishka.integrations.litestar import inject, FromDishka
from litestar import post, get
from litestar.params import Body

from infrastructure.mediator.mediator import Mediator
from application.user.commands.user import CreateUser
from application.user.queries.user import GetUserByOid
from application.user.dto.user import UserDTO, CreateUserDTO


@get("/user/")
@inject
async def read(user_uid: UUID, mediator: FromDishka[Mediator]) -> UserDTO:
    return await mediator.query(GetUserByOid(user_uid))


@post("/user/")
@inject
async def create(
    data: Annotated[CreateUserDTO, Body()], mediator: FromDishka[Mediator]
) -> UUID:
    return await mediator.send(
        CreateUser(username=data.username, password=data.password)
    )
