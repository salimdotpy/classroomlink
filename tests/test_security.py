
import pytest

from app.core.security import hash_password, verify_password


def test_hash_password_returns_argon2id_hash():
    password = "ClassroomLink-Secure-Password"

    hashed_password = hash_password(password)

    assert hashed_password.startswith("$argon2id$")
    assert hashed_password != password


def test_verify_correct_password():
    password = "ClassroomLink-Secure-Password"

    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_verify_incorrect_password():
    hashed_password = hash_password(
        "ClassroomLink-Secure-Password"
    )

    assert verify_password(
        "Wrong-Password",
        hashed_password,
    ) is False


def test_same_password_produces_different_hashes():
    password = "ClassroomLink-Secure-Password"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    # Each hash should use a different random salt.
    assert first_hash != second_hash

    # Both hashes should still verify successfully.
    assert verify_password(password, first_hash) is True
    assert verify_password(password, second_hash) is True


def test_invalid_hash_returns_false():
    assert verify_password(
        "Some-Password",
        "not-a-valid-password-hash",
    ) is False


def test_empty_password_cannot_be_hashed():
    with pytest.raises(ValueError):
        hash_password("")
