
import sqlite3
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url

from app.core.config import BASE_DIR, settings
from app.main import app


def get_database_path() -> Path:
    url = make_url(settings.database_url)

    if url.get_backend_name() != "sqlite":
        raise RuntimeError(
            "These tests expect the configured SQLite database."
        )

    path = Path(url.database)

    if not path.is_absolute():
        path = BASE_DIR / path

    return path


def cleanup_user(email: str) -> None:
    with sqlite3.connect(get_database_path()) as connection:
        connection.execute(
            "DELETE FROM users WHERE email = ?",
            (email,),
        )


def test_login_and_logout():
    email = f"{uuid4().hex}@example.com"
    password = "ClassroomLink-Secure-Password"

    try:
        with TestClient(app) as client:
            # Register an account.
            registration = client.post(
                "/api/v1/auth/register",
                json={
                    "email": email,
                    "password": password,
                },
            )

            assert registration.status_code == 201

            # Login.
            response = client.post(
                "/api/v1/auth/login",
                json={
                    "email": email,
                    "password": password,
                },
            )

            assert response.status_code == 200
            assert response.json()["email"] == email

            # Confirm session cookie was issued.
            assert "classroomlink_session" in client.cookies

            # Verify authenticated identity.
            me_response = client.get("/api/v1/auth/me")

            assert me_response.status_code == 200
            assert me_response.json()["email"] == email

            # Logout.
            logout_response = client.post(
                "/api/v1/auth/logout",
            )

            assert logout_response.status_code == 204

            # Protected endpoint should now reject the request.
            me_after_logout = client.get("/api/v1/auth/me")

            assert me_after_logout.status_code == 401

    finally:
        cleanup_user(email)


def test_login_rejects_incorrect_password():
    email = f"{uuid4().hex}@example.com"

    try:
        with TestClient(app) as client:
            registration = client.post(
                "/api/v1/auth/register",
                json={
                    "email": email,
                    "password": "ClassroomLink-Secure-Password",
                },
            )

            assert registration.status_code == 201

            response = client.post(
                "/api/v1/auth/login",
                json={
                    "email": email,
                    "password": "Incorrect-Password",
                },
            )

            assert response.status_code == 401

    finally:
        cleanup_user(email)


def test_login_rejects_unknown_email():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": f"{uuid4().hex}@example.com",
                "password": "ClassroomLink-Secure-Password",
            },
        )

        assert response.status_code == 401


def test_me_rejects_unauthenticated_request():
    with TestClient(app) as client:
        response = client.get("/api/v1/auth/me")

        assert response.status_code == 401


def test_login_rejects_inactive_account():
    email = f"{uuid4().hex}@example.com"
    password = "ClassroomLink-Secure-Password"

    try:
        with TestClient(app) as client:
            registration = client.post(
                "/api/v1/auth/register",
                json={
                    "email": email,
                    "password": password,
                },
            )

            assert registration.status_code == 201

            with sqlite3.connect(get_database_path()) as connection:
                connection.execute(
                    "UPDATE users SET is_active = 0 WHERE email = ?",
                    (email,),
                )

            response = client.post(
                "/api/v1/auth/login",
                json={
                    "email": email,
                    "password": password,
                },
            )

            assert response.status_code == 401

    finally:
        cleanup_user(email)
