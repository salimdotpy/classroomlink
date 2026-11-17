
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError


# Reuse one password hasher throughout the application.
# recommended() currently uses Argon2.
password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using the recommended
    password-hashing algorithm (Argon2id).

    Returns:
        Encoded password hash.

    Raises:
        ValueError: If the password is empty.
    """

    if not password:
        raise ValueError("Password cannot be empty.")

    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plaintext password against its stored hash.

    Returns:
        True if the password matches.
        False if the password does not match or the
        stored hash cannot be identified.
    """

    if not plain_password or not hashed_password:
        return False

    try:
        return password_hasher.verify(
            plain_password,
            hashed_password,
        )
    except UnknownHashError:
        return False
