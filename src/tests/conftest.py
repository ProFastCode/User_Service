from collections.abc import AsyncIterator

import pytest
from dishka.async_container import AsyncContainer, make_async_container

from src.config import Config
from src.infrastructure.mediator import Mediator
from src.infrastructure.mediator.main import setup_mediator
from src.tests.ioc import TestAppProvider


@pytest.fixture(scope="session")
async def ioc() -> AsyncIterator[AsyncContainer]:
    container = make_async_container(TestAppProvider(), context={"config": Config()})
    async with container() as container:
        yield container
        await container.close()


@pytest.fixture(scope="session")
async def config(ioc: AsyncContainer) -> Config:
    return await ioc.get("config")


@pytest.fixture(scope="session")
async def mediator(ioc: AsyncContainer) -> Mediator:
    mediator = await ioc.get(Mediator)
    await setup_mediator(mediator=mediator, container=ioc)
    return mediator
