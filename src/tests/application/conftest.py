from collections.abc import AsyncIterator

import pytest
from dishka.async_container import AsyncContainer, make_async_container

from application.user.interfaces import UserReader, UserRepo
from infrastructure.mediator import Mediator
from infrastructure.mediator.main import setup_mediator
from infrastructure.memory.repositories import UserReaderMemory, UserRepoMemory
from tests.ioc import TestAppProvider


@pytest.fixture(scope="session")
async def ioc() -> AsyncIterator[AsyncContainer]:
    container = make_async_container(TestAppProvider())
    async with container() as container:
        yield container
        await container.close()


@pytest.fixture(scope="session")
async def mediator(ioc: AsyncContainer) -> Mediator:
    mediator = await ioc.get(Mediator)
    await setup_mediator(mediator=mediator, container=ioc)
    return mediator


@pytest.fixture(scope="session")
async def user_repo(ioc: AsyncContainer) -> UserRepoMemory:
    return await ioc.get(UserRepo)


@pytest.fixture(scope="session")
async def user_reader(ioc: AsyncContainer) -> UserReaderMemory:
    return await ioc.get(UserReader)
