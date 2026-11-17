
from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.dependencies import get_optional_current_user
from app.main import app
from app.models.enums import UserRole
from app.models.user import User


def create_test_user(role: UserRole) -> User:
    return User(
        id=uuid4(),
        email=f"{role.value}-{uuid4().hex[:8]}@example.com",
        password_hash="test-password-hash",
        role=role,
        is_active=True,
    )


def request_as_user(path: str, user: User):
    app.dependency_overrides[get_optional_current_user] = lambda: user

    try:
        with TestClient(app) as client:
            return client.get(path, follow_redirects=False)
    finally:
        app.dependency_overrides.pop(get_optional_current_user, None)


def request_as_anonymous(path: str):
    app.dependency_overrides[get_optional_current_user] = lambda: None

    try:
        with TestClient(app) as client:
            return client.get(path, follow_redirects=False)
    finally:
        app.dependency_overrides.pop(get_optional_current_user, None)


def test_lecturer_dashboard_requires_authentication():
    response = request_as_anonymous("/lecturer/dashboard")

    assert response.status_code == 303
    assert response.headers["location"] == "/"


def test_student_dashboard_requires_authentication():
    response = request_as_anonymous("/student/dashboard")

    assert response.status_code == 303
    assert response.headers["location"] == "/"


def test_lecturer_can_view_lecturer_dashboard():
    user = create_test_user(UserRole.LECTURER)

    response = request_as_user("/lecturer/dashboard", user)

    assert response.status_code == 200
    assert "Lecturer Dashboard" in response.text
    assert user.email in response.text


def test_student_can_view_student_dashboard():
    user = create_test_user(UserRole.STUDENT)

    response = request_as_user("/student/dashboard", user)

    assert response.status_code == 200
    assert "Student Dashboard" in response.text
    assert user.email in response.text


def test_student_cannot_view_lecturer_dashboard():
    user = create_test_user(UserRole.STUDENT)

    response = request_as_user("/lecturer/dashboard", user)

    assert response.status_code == 303
    assert response.headers["location"] == "/student/dashboard"


def test_lecturer_cannot_view_student_dashboard():
    user = create_test_user(UserRole.LECTURER)

    response = request_as_user("/student/dashboard", user)

    assert response.status_code == 303
    assert response.headers["location"] == "/lecturer/dashboard"
