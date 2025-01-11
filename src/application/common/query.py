from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

QR = TypeVar("QR", covariant=True)


@dataclass(frozen=True)
class Query(ABC, Generic[QR]):
    pass


QT = TypeVar("QT", contravariant=True, bound=Query)


@dataclass(frozen=True)
class QueryHandler(Protocol[QT, QR]):
    @abstractmethod
    async def __call__(self, query: QT) -> QR:
        raise NotImplementedError
