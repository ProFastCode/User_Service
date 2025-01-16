from dataclasses import dataclass

from src.application.common.dto import DTO


@dataclass(frozen=True)
class LoginUserDTO(DTO):
    access_token: str
    refresh_token: str
