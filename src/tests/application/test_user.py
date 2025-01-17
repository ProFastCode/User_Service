from src.infrastructure.mediator import Mediator
from src.application.user.commands import RegistrationUser, LoginUser
from src.application.user.queries import GetUserByToken, GetUserByUsername, GetUserByOid


async def test_user_registration(
    mediator: Mediator,
):
    auth_user_dto = await mediator.send(RegistrationUser("qwerty", "Q1w@erty"))
    user = await mediator.query(GetUserByToken(auth_user_dto.access_token))

    assert user
    assert await mediator.query(GetUserByOid(user.oid))
    assert await mediator.query(GetUserByUsername(user.username))


async def test_user_login(mediator: Mediator):
    auth_user_dto = await mediator.send(LoginUser("qwerty", "Q1w@erty"))
    user = await mediator.query(GetUserByToken(auth_user_dto.access_token))

    assert user
    assert await mediator.query(GetUserByOid(user.oid))
    assert await mediator.query(GetUserByUsername(user.username))
