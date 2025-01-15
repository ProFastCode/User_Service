from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol, TypeVar

from src.domain.common import Event

ER = TypeVar("ER", covariant=True)
ET = TypeVar("ET", contravariant=True, bound=Event)


@dataclass
class EventHandler(Protocol[ET, ER]):
    @abstractmethod
    def __call__(self, event: ET) -> ER:
        raise NotImplementedError
