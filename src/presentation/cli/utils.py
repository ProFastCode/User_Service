import asyncio
from functools import wraps
from typing import Callable, Literal

from dishka import make_async_container

from src.infrastructure.ioc import AppProvider
from src.infrastructure.mediator.main import setup_mediator
from src.infrastructure.mediator.mediator import Mediator

container = make_async_container(AppProvider())


def handler(type_: Literal["event", "query", "command"]):
    """
    Декоратор для работы с Mediator.
    :param type_: Тип операции ("event", "query", "command").
    :return: Декоратор, который оборачивает функцию.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            async def _async():
                async with container() as ioc:
                    # Получаем Mediator из контейнера
                    mediator = await ioc.get(Mediator)
                    await setup_mediator(mediator=mediator, container=ioc)

                    # Вызываем функцию для создания команды/запроса/события
                    command = func(*args, **kwargs)

                    # Отправляем команду через Mediator
                    if type_ == "command":
                        await mediator.send(command)
                    elif type_ == "query":
                        result = await mediator.query(command)
                        return result
                    elif type_ == "event":
                        await mediator.publish(command)
                    else:
                        raise ValueError(f"Unsupported type: {type_}")

            # Проверяем, есть ли уже запущенный цикл событий
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop:
                # Если цикл уже запущен, используем его
                return loop.create_task(_async())
            else:
                # Иначе запускаем новый цикл
                return asyncio.run(_async())

        return wrapper

    return decorator
