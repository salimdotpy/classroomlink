
import sqlite3
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url

from app.core.config import BASE_DIR, settings
from app.core.security import verify_password
from app.main import app


def get_database_path() -> Path:
    url = make_url(settings.database_url)

    if url.get_backend_name() != "sqlite":
        raise RuntimeError(
            "These registration tests expect the configured SQLite database."
        )

    path = Path(url.database)

    if not path.is_absolute():
        path = BASE_DIR / path

    return path


def cleanup_user(email: str) -> None:
    """
    Remove a test account after the test completes.
    """

    database_path = get_database_path()

    with sqlite3.connect(database_path) as connection:
        connection.execute(
            "DELETE FROM users WHERE email = ?",
            (email,),
        )


def test_register_lecturer():
    email = f"{uuid4().hex}@example.com"
    password = "ClassroomLink-Secure-Password"

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/auth/register",
                json={
                    "email": email,
                    "password": password,
                },
            )

            assert response.status_code == 201

            data = response.json()

            assert data["email"] == email
            assert data["role"] == "lecturer"
            assert data["is_active"] is True
            assert "id" in data
            assert "password_hash" not in data

            # Confirm duplicate registration is rejected.
            duplicate_response = client.post(
                "/api/v1/auth/register",
                json={
                    "email": email,
                    "password": password,
                },
            )

            assert duplicate_response.status_code == 409

            # Verify that the stored password is an Argon2id hash.
            with sqlite3.connect(get_database_path()) as connection:
                row = connection.execute(
                    """
                    SELECT password_hash, role
                    FROM users
                    WHERE email = ?
                    """,
                    (email,),
                ).fetchone()

            assert row is not None

            stored_hash, stored_role = row

            assert stored_hash.startswith("$argon2id$")
            assert verify_password(password, stored_hash)
            assert stored_role == "lecturer"

    finally:
        cleanup_user(email)


def test_registration_rejects_invalid_input():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "not-a-valid-email",
                "password": "short",
            },
        )

        assert response.status_code == 422


def test_registration_rejects_role_override():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": f"{uuid4().hex}@example.com",
                "password": "ClassroomLink-Secure-Password",
                "role": "student",
            },
        )

        assert response.status_code == 422
