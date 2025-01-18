from dataclasses import dataclass

from src.application.common.dto import DTO
from src.application.token.dto import TokenDTO


@dataclass(frozen=True)
class TokenPairDTO(DTO):
    access_token: TokenDTO
    refresh_token: TokenDTO
