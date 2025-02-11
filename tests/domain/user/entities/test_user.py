import pytest

from src.domain.user.entities.user import UserEntity
from src.domain.user.exceptions.entities.user import InvalidUsernameOrPasswordError


def test_create():
    user = UserEntity.create("john_doe", "SecureP@ss1")
    assert user


def test_check_password():
    user = UserEntity.create("john_doe", "SecureP@ss1")

    assert user.check_password("SecureP@ss1") is None

    with pytest.raises(InvalidUsernameOrPasswordError):
        user.check_password("SecureP@ss2")


def test_change_pasword():
    user = UserEntity.create("john_doe", "SecureP@ss1")

    assert user.check_password("SecureP@ss1") is None

    user.change_password("SecureP@ss2")

    assert user.check_password("SecureP@ss2") is None

    with pytest.raises(InvalidUsernameOrPasswordError):
        user.check_password("SecureP@ss1")
