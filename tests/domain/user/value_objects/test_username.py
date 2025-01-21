import pytest

from src.domain.user.exceptions.value_objects.username import (
    UsernameTooLongError, UsernameTooShortError, WrongUsernameFormatError)
from src.domain.user.value_objects.username import Username


def test_valid_username():
    username = Username("john_doe")
    assert username.to_raw() == "john_doe"


def test_username_too_short():
    with pytest.raises(UsernameTooShortError):
        Username("jo")


def test_username_too_long():
    with pytest.raises(UsernameTooLongError):
        Username("a" * 33)


def test_wrong_username_format():
    with pytest.raises(WrongUsernameFormatError):
        Username("123_john")
