import typer

from dishka import make_async_container

from src.infrastructure.ioc import AppProvider
from src.application.user.commands.login_user import LoginUser
from src.application.user.commands.registration_user import RegistrationUser
from src.presentation.cli.utils import handler


app = typer.Typer()


container = make_async_container(AppProvider())


@app.command(name="register")
@handler("command")
def registration(
    username: str,
    password: str,
):
    return RegistrationUser(username=username, password=password)


@app.command()
@handler("command")
def login(username: str, password: str):
    return LoginUser(username=username, password=password)


if __name__ == "__main__":
    app()
