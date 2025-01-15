from collections.abc import Sequence

from src.application.common.interfaces.uow import UnitOfWork


def build_uow() -> UnitOfWork:
    uow = UnitOfWorkImpl(())
    return uow


class UnitOfWorkImpl(UnitOfWork):
    def __init__(self, uows: Sequence[UnitOfWork]) -> None:
        self._uows = uows

    async def commit(self) -> None:
        for uow in self._uows:
            await uow.commit()

    async def rollback(self) -> None:
        for uow in self._uows:
            await uow.rollback()
