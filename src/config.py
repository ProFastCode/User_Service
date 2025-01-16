import os
from dotenv import load_dotenv
from typing import Any, Optional

load_dotenv()


class Config:
    def __init__(self) -> None:
        self.JWT_SECRET = self.get_env_var("JWT_SECRET", "default_secret_key")
        self.DEBUG = self.get_env_var("DEBUG", False, bool)
        self.PORT = self.get_env_var("PORT", 8000, int)

    @staticmethod
    def get_env_var(key: str, default: Any = None, cast: Optional[type] = None) -> Any:
        value = os.getenv(key, default)
        if value is None:
            return default
        if cast:
            if cast is bool and type(value) is not bool:
                return value.lower() in {"true", "1", "yes"}
            try:
                return cast(value)
            except ValueError:
                raise ValueError(
                    f"Не удалось преобразовать переменную окружения '{key}' в тип {cast}"
                )
        return value
