from abc import ABC
from dataclasses import dataclass, field
from time import time
from uuid import UUID, uuid4


@dataclass
class Entity(ABC):
    pass


@dataclass
class UUIDEntity(ABC):
    oid: UUID = field(init=False, kw_only=True, default_factory=uuid4)


@dataclass
class CreatedAtEntity(ABC):
    created_at: int = field(
        init=False, kw_only=True, default_factory=lambda: int(time())
    )
