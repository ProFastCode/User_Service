from dataclasses import dataclass

from src.application.common.dto import DTO


@dataclass(frozen=True)
class TokenPairDTO(DTO):
    access_token: str
    refresh_token: str
