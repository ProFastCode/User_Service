from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

V = TypeVar("V", bound=Any)


@dataclass(frozen=True)
class ValueObject(ABC, Generic[V]):
    value: V

    def __post_init__(self) -> None:
        self._validate()

    @abstractmethod
    def _validate(self) -> None:
        raise NotImplementedError

    def to_raw(self) -> V:
        return self.value
