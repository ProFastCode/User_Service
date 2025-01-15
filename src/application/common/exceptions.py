from src.domain.common import AppError


class ApplicationError(AppError):
    @property
    def detail(self) -> str:
        return "An application error occurred"
