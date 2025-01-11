from litestar import Litestar
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin


def get_litestar_app() -> Litestar:
    litestar_app = Litestar(
        openapi_config=OpenAPIConfig(
            title="User Service",
            description="User Service",
            version="0.0.1",
            render_plugins=[SwaggerRenderPlugin()],
        ),
    )

    return litestar_app
