from dataclasses import dataclass
from typing import ClassVar


@dataclass(eq=False)
class AppError(Exception):
    status: ClassVar[int] = 500

    @property
    def detail(self) -> str:
        return "An app error occurred"


class DomainError(AppError):
    @property
    def detail(self) -> str:
        return "A domain error occurred"
