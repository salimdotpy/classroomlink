from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session
from app.schemas.user import UserRead, UserRegister
from app.services.auth import (
    AuthService,
    EmailAlreadyRegisteredError,
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a lecturer account",
)
async def register_lecturer(
    data: UserRegister,
    session: AsyncSession = Depends(get_session),
):
    """
    Register a new lecturer account.

    Public registration always creates lecturer accounts.
    """

    service = AuthService(session)

    try:
        user = await service.register_lecturer(data)

    except EmailAlreadyRegisteredError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    return user
