from dataclasses import dataclass
from typing import ClassVar


@dataclass(eq=False)
class AppError(Exception):
    status: ClassVar[int] = 500

    @property
    def message(self) -> str:
        return "An app error occurred"


class DomainError(AppError):
    @property
    def message(self) -> str:
        return "A domain error occurred"


class ValueObjectError(DomainError):
    @property
    def message(self) -> str:
        return "An error occurred in a value object"
