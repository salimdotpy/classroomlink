import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown.
    """

    logger.info(
        "Starting %s in %s mode",
        settings.app_name,
        settings.app_env,
    )

    # Verify database connectivity.
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))

    logger.info("Database connection established successfully.")

    try:
        yield

    finally:
        await engine.dispose()

        logger.info("Database connections released.")
        logger.info("%s shutdown complete.", settings.app_name)