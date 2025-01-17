from litestar import Request
from litestar.enums import ScopeType
from litestar.types import ASGIApp, Scope, Receive, Send

from src.infrastructure.mediator import Mediator
from src.infrastructure.mediator.main import setup_mediator


def add_request_container_middleware(app: ASGIApp) -> ASGIApp:
    async def middleware(scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get("type") != ScopeType.HTTP:
            await app(scope, receive, send)
            return

        request = Request(scope)
        async with request.app.state.dishka_container(
            {Request: request},
        ) as request_container:
            mediator = await request_container.get(Mediator)
            await setup_mediator(mediator=mediator, container=request_container)
            request.state.dishka_container = request_container
            await app(scope, receive, send)

    return middleware
