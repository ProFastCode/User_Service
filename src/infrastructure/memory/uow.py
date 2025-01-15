from src.application.common.interfaces.uow import UnitOfWork


class MemoryUoW(UnitOfWork):
    def __init__(self) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
