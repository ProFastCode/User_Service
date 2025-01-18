from dataclasses import dataclass

from src.application.common.dto import DTO
from src.application.token.constants import TokenType


@dataclass(frozen=True)
class TokenDTO(DTO):
    token: str
    exp: float
    token_type: TokenType
