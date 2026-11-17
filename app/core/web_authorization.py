
from fastapi import Depends, HTTPException, Request, status

from app.core.dependencies import get_optional_current_user
from app.models.enums import UserRole
from app.models.user import User


async def get_current_lecturer_page(
    request: Request,
    current_user: User | None = Depends(get_optional_current_user),
) -> User:
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/"},
        )

    if current_user.role != UserRole.LECTURER:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/student/dashboard"},
        )

    return current_user


async def get_current_student_page(
    request: Request,
    current_user: User | None = Depends(get_optional_current_user),
) -> User:
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/"},
        )

    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/lecturer/dashboard"},
        )

    return current_user
