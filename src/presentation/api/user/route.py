from typing import Annotated

from dishka.integrations.litestar import FromDishka, inject
from litestar import Router, get, post
from litestar.params import Body

from src.application.token.dto import TokenPairDTO
from src.application.token.queries import GetOidToken
from src.application.user.commands import LoginUser, RegistrationUser
from src.application.user.queries.get_user_by_oid import GetUserByOid
from src.infrastructure.mediator import Mediator

from .schemas import ResponseUserDTO


@post("/registration", request_model=RegistrationUser, response_model=TokenPairDTO)
@inject
async def registration(
    data: Annotated[RegistrationUser, Body()], mediator: FromDishka[Mediator]
) -> TokenPairDTO:
    return await mediator.send(data)


@post("/login", request_model=LoginUser, response_model=TokenPairDTO)
@inject
async def login(
    data: Annotated[LoginUser, Body()], mediator: FromDishka[Mediator]
) -> TokenPairDTO:
    return await mediator.send(data)


@get(response_model=ResponseUserDTO)
@inject
async def read(access_token: str, mediator: FromDishka[Mediator]) -> ResponseUserDTO:
    oid = await mediator.query(GetOidToken(access_token))
    result = await mediator.query(GetUserByOid(oid))
    return ResponseUserDTO(
        oid=result.oid,
        username=result.username,
    )


router = Router("/users", tags=["users"], route_handlers=[registration, login, read])
