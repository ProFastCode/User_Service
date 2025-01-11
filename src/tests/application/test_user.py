from infrastructure.mediator import Mediator
from application.user.commands import CreateUser
from application.user.interfaces import UserReader


async def test_user_create(
    mediator: Mediator,
    user_reader: UserReader,
):
    user_oid = await mediator.send(CreateUser("qwerty", "Q1w@erty"))

    assert await user_reader.get_by_oid(user_oid=user_oid)
