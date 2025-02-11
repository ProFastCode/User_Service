from litestar import get


@get("/ping")
def ping() -> dict:
    return {"ping": "pong from Artix!"}
