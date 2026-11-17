
from uuid import UUID

from app.models.enums import UserRole
from app.models.user import User
from app.schemas.user import UserRead


def test_user_model_creation():
    user = User(
        email="lecturer@example.com",
        password_hash="test-hash",
        role=UserRole.LECTURER,
    )

    assert isinstance(user.id, UUID)
    assert user.email == "lecturer@example.com"
    assert user.role == UserRole.LECTURER
    assert user.is_active is True
    assert user.created_at is not None
    assert user.updated_at is not None


def test_student_role():
    user = User(
        email="student@example.com",
        password_hash="test-hash",
        role=UserRole.STUDENT,
    )

    assert user.role == UserRole.STUDENT


def test_user_read_schema_excludes_password_hash():
    user = User(
        email="lecturer@example.com",
        password_hash="secret-hash",
        role=UserRole.LECTURER,
    )

    result = UserRead.model_validate(user)

    assert result.email == "lecturer@example.com"
    assert result.role == UserRole.LECTURER
    assert "password_hash" not in result.model_dump()
