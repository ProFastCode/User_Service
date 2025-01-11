from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

CR = TypeVar("CR", covariant=True)


@dataclass(frozen=True)
class Command(ABC, Generic[CR]):
    pass


CT = TypeVar("CT", contravariant=True, bound=Command)


@dataclass(frozen=True)
class CommandHandler(Protocol[CT, CR]):
    @abstractmethod
    async def __call__(self, command: CT) -> CR:
        raise NotImplementedError
