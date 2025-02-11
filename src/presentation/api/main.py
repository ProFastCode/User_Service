import logging

from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin

from src.domain.common.exceptions import AppError
from src.infrastructure.ioc import AppProvider
from src.presentation.api.exception_handlers import app_error_handler
from src.presentation.api.middleware import add_request_container_middleware

from .user import user_router

logger = logging.getLogger(__name__)

ioc = make_async_container(AppProvider())


def get_litestar_app() -> Litestar:
    litestar_app = Litestar(
        [user_router],
        middleware=[add_request_container_middleware],
        openapi_config=OpenAPIConfig(
            title="User Service",
            description="User Service",
            version="0.0.1",
            render_plugins=[SwaggerRenderPlugin()],
            path="/docs",
        ),
        exception_handlers={
            AppError: app_error_handler,
        },
    )
    litestar_integration.setup_dishka(ioc, litestar_app)
    return litestar_app
