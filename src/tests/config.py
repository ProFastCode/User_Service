from typing import Optional


class TestConfig:
    def __init__(self):
        self.JWT_SECRET = self.get_env_var("JWT_SECRET", default="default_secret_key")

    @staticmethod
    def get_env_var(key: str, default=None, required: bool = False) -> Optional[str]:
        value = default
        if required and value is None:
            raise ValueError(f"Обязательная переменная окружения '{key}' не найдена.")
        return value
