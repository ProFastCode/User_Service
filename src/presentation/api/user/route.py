from typing import Annotated
from uuid import UUID

from litestar.params import Body
from litestar import post, get, Router
from dishka.integrations.litestar import inject, FromDishka

from src.application.user.dto.user import UserDTO

from .schemas import ResponseUserDTO, RequestCreateUserDTO
from src.application.user.commands import CreateUser
from src.application.user.queries import GetUserByToken
from src.infrastructure.mediator import Mediator


@get(response_model=ResponseUserDTO)
@inject
async def read(access_token: str, mediator: FromDishka[Mediator]) -> UserDTO:
    return await mediator.query(GetUserByToken(access_token))


@post(request_model=RequestCreateUserDTO)
@inject
async def create(
    data: Annotated[RequestCreateUserDTO, Body()], mediator: FromDishka[Mediator]
) -> UUID:
    return await mediator.send(
        CreateUser(
            username=data.username,
            password=data.password,
        )
    )


router = Router("/users", tags=["users"], route_handlers=[read, create])
