
import asyncio
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.core.authorization import (
    get_current_classroom_user,
    get_current_lecturer,
    get_current_student,
    require_roles,
)
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


def test_lecturer_can_access_lecturer_resources():
    user = create_test_user(UserRole.LECTURER)

    result = asyncio.run(
        get_current_lecturer(current_user=user)
    )

    assert result is user


def test_student_can_access_student_resources():
    user = create_test_user(UserRole.STUDENT)

    result = asyncio.run(
        get_current_student(current_user=user)
    )

    assert result is user


def test_student_cannot_access_lecturer_resources():
    user = create_test_user(UserRole.STUDENT)

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            get_current_lecturer(current_user=user)
        )

    assert exc_info.value.status_code == 403


def test_lecturer_cannot_access_student_resources():
    user = create_test_user(UserRole.LECTURER)

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            get_current_student(current_user=user)
        )

    assert exc_info.value.status_code == 403


def test_both_roles_can_access_classroom_resources():
    lecturer = create_test_user(UserRole.LECTURER)
    student = create_test_user(UserRole.STUDENT)

    lecturer_result = asyncio.run(
        get_current_classroom_user(current_user=lecturer)
    )

    student_result = asyncio.run(
        get_current_classroom_user(current_user=student)
    )

    assert lecturer_result is lecturer
    assert student_result is student


def test_role_dependency_requires_at_least_one_role():
    with pytest.raises(ValueError):
        require_roles()
