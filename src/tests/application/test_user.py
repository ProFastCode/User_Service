from src.infrastructure.mediator import Mediator
from src.application.user.commands import CreateUser, LoginUser
from src.application.user.queries import GetUserByToken, GetUserByUsername, GetUserByOid


async def test_user_create(
    mediator: Mediator,
):
    user_oid = await mediator.send(CreateUser("qwerty", "Q1w@erty"))

    assert await mediator.query(GetUserByOid(user_oid))
    assert await mediator.query(GetUserByUsername("qwerty"))


async def test_user_login(mediator: Mediator):
    login_user_dto = await mediator.send(LoginUser("qwerty", "Q1w@erty"))

    assert await mediator.query(GetUserByToken(login_user_dto.access_token))
