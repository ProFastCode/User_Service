from src.domain.user.entities.user import User


def test_create():
    user = User.create("john_doe", "SecureP@ss1")
    assert user


def test_check_pasword():
    user = User.create("john_doe", "SecureP@ss1")
    assert user.check_password("SecureP@ss1")


def test_change_pasword():
    user = User.create("john_doe", "SecureP@ss1")
    user.change_password("SecureP@ss2")
    assert user.check_password("SecureP@ss2")
