
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# Create the asynchronous database engine.
engine = create_async_engine(
    settings.database_url,
    echo=settings.sql_echo,
    connect_args=(
        {
            "check_same_thread": False,
            "timeout": 30,
        }
        if settings.database_url.startswith("sqlite")
        else {}
    ),
)

# Create an asynchronous session factory.
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)