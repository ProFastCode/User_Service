import pytest

from src.domain.user.exceptions.value_objects.password import (
    PasswordRequiresDigitError,
    PasswordRequiresLowercaseError,
    PasswordRequiresSpecialCharError,
    PasswordRequiresUppercaseError,
    PasswordTooLongError,
    PasswordTooShortError,
)
from src.domain.user.value_objects.password import Password


def test_valid_password():
    password = Password("SecureP@ss1")
    assert password.to_raw() == "SecureP@ss1"


def test_password_too_short():
    with pytest.raises(PasswordTooShortError):
        Password("Short1")


def test_password_too_long():
    with pytest.raises(PasswordTooLongError):
        Password("a" * 65)


def test_password_requires_digit():
    with pytest.raises(PasswordRequiresDigitError):
        Password("NoDigits!")


def test_password_requires_uppercase():
    with pytest.raises(PasswordRequiresUppercaseError):
        Password("nouppercase1!")


def test_password_requires_lowercase():
    with pytest.raises(PasswordRequiresLowercaseError):
        Password("NOLOWERCASE1!")


def test_password_requires_special_char():
    with pytest.raises(PasswordRequiresSpecialCharError):
        Password("NoSpecialChar1")
