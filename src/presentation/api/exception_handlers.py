import logging

from litestar import Request, Response

from src.domain.common.exceptions import AppError


def app_error_handler(request: Request, exc: AppError) -> Response:
    logging.error(exc.message)
    return Response(
        content={"message": exc.message},
        status_code=exc.status,
    )
