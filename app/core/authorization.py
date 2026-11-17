
from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.models.enums import UserRole
from app.models.user import User


def require_roles(*allowed_roles: UserRole):
    """
    Create a dependency that restricts access to specified user roles.
    """

    if not allowed_roles:
        raise ValueError("At least one allowed role must be specified.")

    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )

        return current_user

    return role_checker


# Lecturer-only access
get_current_lecturer = require_roles(UserRole.LECTURER)

# Student-only access
get_current_student = require_roles(UserRole.STUDENT)

# Access for either lecturer or student
get_current_classroom_user = require_roles(
    UserRole.LECTURER,
    UserRole.STUDENT,
)
