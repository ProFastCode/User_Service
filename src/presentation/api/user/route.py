from typing import Annotated

from litestar.params import Body
from litestar import post, get, Router
from dishka.integrations.litestar import inject, FromDishka

from src.application.user.dto.user import AuthUserDTO
from src.application.user.commands import RegistrationUser, LoginUser
from src.application.user.queries import GetUserByToken
from src.infrastructure.mediator import Mediator
from .schemas import ResponseUserDTO


@post("/registration", request_model=RegistrationUser, response_model=AuthUserDTO)
@inject
async def registration(
    data: Annotated[RegistrationUser, Body()], mediator: FromDishka[Mediator]
) -> AuthUserDTO:
    return await mediator.send(data)


@post("/login", request_model=LoginUser, response_model=AuthUserDTO)
@inject
async def login(
    data: Annotated[LoginUser, Body()], mediator: FromDishka[Mediator]
) -> AuthUserDTO:
    return await mediator.send(data)


@get(response_model=ResponseUserDTO)
@inject
async def read(access_token: str, mediator: FromDishka[Mediator]) -> ResponseUserDTO:
    result = await mediator.query(GetUserByToken(access_token))
    return ResponseUserDTO(
        oid=result.oid,
        username=result.username,
    )


router = Router("/users", tags=["users"], route_handlers=[registration, login, read])
