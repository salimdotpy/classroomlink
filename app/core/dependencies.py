
from collections.abc import AsyncGenerator
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import SessionLocal
from app.models.user import User
from app.repositories.user import UserRepository


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_optional_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> User | None:
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    try:
        parsed_user_id = UUID(str(user_id))
    except (ValueError, TypeError):
        request.session.clear()
        return None

    repository = UserRepository(session)
    user = await repository.get_by_id(parsed_user_id)

    if user is None or not user.is_active:
        request.session.clear()
        return None

    return user


async def get_current_user(
    current_user: User | None = Depends(get_optional_current_user),
) -> User:
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    return current_user
