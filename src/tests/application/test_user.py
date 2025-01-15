from src.infrastructure.mediator import Mediator
from src.application.user.commands import CreateUser
from src.application.user.interfaces import UserReader


async def test_user_create(
    mediator: Mediator,
    user_reader: UserReader,
):
    user_oid = await mediator.send(CreateUser("qwerty", "Q1w@erty"))

    assert await user_reader.get_by_oid(user_oid=user_oid)
