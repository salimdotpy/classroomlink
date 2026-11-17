
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import SessionLocal

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session.

    The session is automatically closed after
    the request has completed.
    """

    async with SessionLocal() as session:
        yield session