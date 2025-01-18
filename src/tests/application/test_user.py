from src.application.token.commands.refresh_token import RefreshToken
from src.infrastructure.mediator import Mediator
from src.application.user.commands import RegistrationUser, LoginUser
from src.application.user.queries import GetUserByUsername, GetUserByOid
from src.application.token.queries import GetOidToken
from src.application.token.constants import TokenType


async def test_user_registration(
    mediator: Mediator,
):
    token_pair_dto = await mediator.send(RegistrationUser("qwerty", "Q1w@erty"))
    oid = await mediator.query(
        GetOidToken(token_pair_dto.access_token.token, TokenType.ACCESS)
    )
    assert oid

    user = await mediator.query(GetUserByOid(oid))

    assert user

    assert await mediator.query(GetUserByUsername(user.username))


async def test_user_login(mediator: Mediator):
    token_pair_dto = await mediator.send(LoginUser("qwerty", "Q1w@erty"))
    oid = await mediator.query(
        GetOidToken(token_pair_dto.access_token.token, TokenType.ACCESS)
    )
    assert oid

    user = await mediator.query(GetUserByOid(oid))

    assert user

    assert await mediator.query(GetUserByUsername(user.username))


async def test_user_refresh_token(mediator: Mediator):
    token_pair_dto = await mediator.send(LoginUser("qwerty", "Q1w@erty"))
    oid = await mediator.query(
        GetOidToken(token_pair_dto.access_token.token, TokenType.ACCESS)
    )
    assert oid

    access_token = await mediator.send(RefreshToken(token_pair_dto.refresh_token.token))
    assert access_token

    oid = await mediator.query(GetOidToken(access_token.token, TokenType.ACCESS))
    assert oid

    user = await mediator.query(GetUserByOid(oid))

    assert user

    assert await mediator.query(GetUserByUsername(user.username))
