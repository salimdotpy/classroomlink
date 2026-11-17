
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import (
    get_current_user,
    get_session,
)
from app.models.user import User
from app.schemas.user import (
    UserLogin,
    UserRead,
    UserRegister,
)
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


@router.post(
    "/login",
    response_model=UserRead,
    summary="Authenticate a user",
)
async def login(
    data: UserLogin,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """
    Authenticate a user and establish a session.
    """

    service = AuthService(session)

    user = await service.authenticate_user(data)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Session"},
        )

    # Clear any previous session data before establishing
    # a new authenticated session.
    request.session.clear()

    request.session["user_id"] = str(user.id)

    return user


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Log out the current user",
)
async def logout(request: Request):
    """
    Clear the current authenticated session.
    """

    request.session.clear()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/me",
    response_model=UserRead,
    summary="Get the current authenticated user",
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Return information about the authenticated user.
    """

    return current_user
