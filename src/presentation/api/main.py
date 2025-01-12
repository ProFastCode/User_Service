import logging
from litestar import Litestar, Request, Response
from litestar.enums import ScopeType
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin

from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration

from litestar.types import ASGIApp, Scope, Receive, Send
from infrastructure.ioc import AppProvider
from infrastructure.mediator import Mediator
from infrastructure.mediator.main import setup_mediator
from domain.common.exception import AppError

from .user import route as user_route

ioc = make_async_container(AppProvider())

logger = logging.getLogger(__name__)


def app_error_handler(request: Request, exc: AppError) -> Response:
    logging.error(exc.message)
    return Response(
        content={"message": exc.message},
        status_code=400,
    )


def add_request_container_middleware(app: ASGIApp) -> ASGIApp:
    async def middleware(scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get("type") != ScopeType.HTTP:
            await app(scope, receive, send)
            return

        request = Request(scope)  # type: ignore[var-annotated]
        async with request.app.state.dishka_container(
            {Request: request},
        ) as request_container:
            mediator = await request_container.get(Mediator)
            await setup_mediator(mediator=mediator, container=request_container)
            request.state.dishka_container = request_container
            await app(scope, receive, send)

    return middleware


def get_litestar_app() -> Litestar:
    litestar_app = Litestar(
        [user_route.read, user_route.create],
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
