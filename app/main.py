from app.routers import auth_router
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import BASE_DIR, settings
from app.core.dependencies import get_session
from app.core.exceptions import register_exception_handlers
from app.core.lifespan import lifespan
from app.core.templates import templates

STATIC_DIR = BASE_DIR / "app" / "static"

app = FastAPI(
    title=settings.app_name,
    description=(
        "A local network-based interactive classroom "
        "screen-sharing and laboratory streaming system."
    ),
    version="0.2.0",
    debug=settings.debug,
    lifespan=lifespan,
)

# Register centralized exception handlers.
register_exception_handlers(app)

app.include_router(auth_router)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Serve local CSS, JavaScript, and images.
app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)

@app.get(
    "/",
    response_class=HTMLResponse,
    tags=["General"],
)
async def home(request: Request):
    """
    Render the ClassroomLink homepage.
    """

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "app_name": settings.app_name,
        },
    )

@app.get(
    "/health",
    tags=["General"],
)
async def health_check(
    session: AsyncSession = Depends(get_session),
):
    """
    Check application and database health.
    """

    await session.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": "0.2.0",
        "database": "connected",
    }